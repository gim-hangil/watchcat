import datetime
import dotenv
import logging
import os
import requests
import requests.exceptions
import sqlmodel
from collections.abc import Sequence
from . import db


logger = logging.getLogger()


class WeatherAPI:
    """Korea Meteorological Administration (KMA) weather API.

    Wrapper class for KMA weather API. It provides methods to fetch ASOS and
    station data from the API and save them to the database.

    Attributes:
        BASE_URL: The base URL of the KMA API.
        KST_TIMEZONE: The timezone of Korea Standard Time (KST).
        auth_key: The key authorized by KMA API hub.
    """

    BASE_URL = "https://apihub.kma.go.kr/api/typ01"
    KST_TIMEZONE = datetime.timezone(datetime.timedelta(hours=9), name="KST")

    def __init__(self, auth_key: str | None = None):
        """Initilize the instance with auth key

        Args:
            auth_key: The key authorized by KMA API hub. If not provided, it
                will be loaded from environmental variable.
        """
        if auth_key == None:
            dotenv.load_dotenv()
            auth_key = os.environ.get("KMA_AUTH_KEY", "")
        self.auth_key: str = auth_key

    def fetch_asos(
        self,
        session: db.SessionDep,
        time_from: int,
        time_to: int = 0,
    ) -> Sequence[db.ASOS]:
        """Fetch ASOS data from the API or the database.

        Try to read ASOS data from the database first. If the data is not found
        or partially missing, it will fetch the data from the API and save it to
        the database.

        Args:
            session: The database session.
            time_from: The start timestamp of the data to fetch.
            time_to: The end timestamp of the data to fetch. If not provided, it
                will be set to the current timestamp.

        Returns:
            A sequence of ASOS data rows.
        """
        # TODO: After implementing _read_asos method, this method should call
        # _read_asos first and catch exception to get ASOS data from the API.
        # Currently this method always gets ASOS data from the API.
        logger.info("Fetching ASOS")
        return self._get_asos(session, time_from, time_to)

    def fetch_pm10(
        self, session: db.SessionDep, tm1: int, tm2: int = 0
    ) -> Sequence[db.PM]:
        logger.info("Fetching PM10")
        return self._get_pm10(session, tm1, tm2)

    def fetch_station(
        self, session: db.SessionDep, timestamp: int
    ) -> Sequence[db.Station]:
        logger.info("Fetching station")
        try:
            stations = self._read_station(session, timestamp)
        except EOFError:
            stations = self._get_station(session, timestamp)
        return stations

    def _get_station(
        self,
        session: db.SessionDep,
        timestamp: int = 0,
    ) -> Sequence[db.Station]:
        logger.info("Requesting station data to KMA API")
        try:
            response = self._request_station()
        except requests.exceptions.Timeout, requests.exceptions.ConnectionError:
            logger.info("Failed to get station data from KMA API")
            return []
        rows = db.Station.from_strs(response.text.split("\n"), timestamp)
        self._save_station(session, rows, timestamp)
        return rows

    def _get_asos(
        self,
        session: db.SessionDep,
        time_from: int = 0,
        time_to: int = 0,
    ) -> Sequence[db.ASOS]:
        logger.info("Requesting ASOS data to KMA API")
        try:
            response = self._request_asos(time_from, time_to)
        except requests.exceptions.Timeout, requests.exceptions.ConnectionError:
            logger.info("Failed to get ASOS data from KMA API")
            return []
        rows = db.ASOS.from_strs(response.text.split("\n"))
        self._save_asos(session, rows)
        return rows

    def _read_asos(
        self,
        session: db.SessionDep,
        time_from: int,
        time_to: int,
    ) -> Sequence[db.ASOS]:
        logger.info("Reading ASOS data from the database")
        # TODO: Check whether ASOS data of given time range is exist in the DB
        # and return if exist else raise exception to get data from the API.
        raise NotImplementedError

    def _read_station(
        self, session: db.SessionDep, timestamp: int
    ) -> Sequence[db.Station]:
        logger.info("Reading station data from the database")
        stations = session.exec(
            sqlmodel.select(db.Station)
            .where(db.Station.timestamp - timestamp <= 12 * 60 * 60)
            .where(db.Station.timestamp - timestamp >= -12 * 60 * 60)
        ).all()
        if len(stations) == 0:
            logger.info("Failed to read station data from the database")
            raise EOFError("Station data not found in the database.")
        return stations

    def _save_asos(self, session: db.SessionDep, rows: Sequence[db.ASOS]):
        logger.info("Saving ASOS data to the database")
        for row in rows:
            if (
                session.exec(
                    sqlmodel.select(db.ASOS).where(
                        db.ASOS.timestamp == row.timestamp,
                        db.ASOS.station_id == row.station_id,
                    )
                ).first()
                is not None
            ):
                continue
            session.add(row)
            session.commit()

    def _save_station(
        self, session: db.SessionDep, rows: Sequence[db.Station], timestamp: int
    ):
        logger.info("Saving station data to the database")
        for row in rows:
            if (
                session.exec(
                    sqlmodel.select(db.Station).where(
                        db.Station.id == row.id, db.Station.timestamp == timestamp
                    )
                ).first()
                is not None
            ):
                continue
            row.timestamp = timestamp
            session.add(row)
            session.commit()

    def _get_pm10(
        self,
        session: db.SessionDep,
        time_from: int = 0,
        time_to: int = 0,
    ) -> Sequence[db.PM]:
        logger.info("Requesting PM10 data to KMA API")
        try:
            response = self._request_pm10(time_from, time_to)
        except requests.exceptions.Timeout, requests.exceptions.ConnectionError:
            logger.info("Failed to get PM10 data from KMA API")
            return []
        rows = db.PM.from_strs(response.text.split("\n"))
        self._save_pm10(session, rows)
        return rows

    def _save_pm10(self, session: db.SessionDep, rows: Sequence[db.PM]):
        logger.info("Saving PM10 data to the database")
        for row in rows:
            if (
                session.exec(
                    sqlmodel.select(db.PM).where(
                        db.PM.timestamp == row.timestamp,
                        db.PM.station_id == row.station_id,
                    )
                ).first()
                is not None
            ):
                continue
            session.add(row)
            session.commit()

    def _request_asos(
        self,
        time_from: int = 0,
        time_to: int = 0,
    ) -> requests.Response:
        logger.info("Requesting ASOS data to KMA API")
        # Possibly raise requests.exceptions.Timeout
        tm1 = self.KST_datetime_from_timestamp(time_from)
        tm2 = self.KST_datetime_from_timestamp(time_to)
        url = self.BASE_URL + "/url/kma_sfctm3.php"
        params = {
            "authKey": self.auth_key,
            "tm1": tm1.strftime("%Y%m%d%H00"),
            "tm2": tm2.strftime("%Y%m%d%H00"),
            "stn": 0,
        }
        return requests.get(url, params=params, timeout=3)

    def _request_pm10(
        self,
        time_from: int = 0,
        time_to: int = 0,
    ) -> requests.Response:
        logger.info("Requesting PM10 data to KMA API")
        tm1 = self.KST_datetime_from_timestamp(time_from)
        tm2 = self.KST_datetime_from_timestamp(time_to)
        url = self.BASE_URL + "/url/kma_pm10.php"
        params = {
            "authKey": self.auth_key,
            "tm1": tm1.strftime("%Y%m%d%H00"),
            "tm2": tm2.strftime("%Y%m%d%H00"),
            "stn": 0,
        }
        return requests.get(url, params=params, timeout=3)

    def _request_station(self, timestamp: int = 0) -> requests.Response:
        tm = self.KST_datetime_from_timestamp(timestamp)
        url = self.BASE_URL + "/url/stn_inf.php"
        params = {
            "authKey": self.auth_key,
            "tm": tm.strftime("%Y%m%d%H00"),
            "inf": "SFC",
        }
        logger.info("Requesting station data to KMA API")
        return requests.get(url, params=params, timeout=3)

    @classmethod
    def KST_datetime_from_timestamp(cls, timestamp: int) -> datetime.datetime:
        if timestamp <= 0:
            return datetime.datetime.now(cls.KST_TIMEZONE)
        return datetime.datetime.fromtimestamp(timestamp, cls.KST_TIMEZONE)

    @classmethod
    def timestamp_from_KST_string(cls, kst_string: str) -> int:
        return int(datetime.datetime.strptime(kst_string, "%Y%m%d%H%M").timestamp())
