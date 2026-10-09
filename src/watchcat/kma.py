import datetime
import dotenv
import os
import re
import requests
import requests.exceptions
import sqlmodel
from typing import Sequence
from . import db


class WeatherAPI:
    BASE_URL = "https://apihub.kma.go.kr/api/typ01"
    KST_TIMEZONE = datetime.timezone(datetime.timedelta(hours=9), name="KST")

    def __init__(self, auth_key: str = ""):
        if auth_key == "":
            dotenv.load_dotenv()
            auth_key = os.environ.get("KMA_AUTH_KEY", "")
        self.auth_key = auth_key

    def fetch_asos(
        self,
        session: db.SessionDep,
        time_from: int,
        time_to: int = 0,
    ) -> Sequence[db.ASOS]:
        # TODO: After implementing _read_asos method, this method should call
        # _read_asos first and catch exception to get ASOS data from the API.
        # Currently this method always gets ASOS data from the API.
        return self._get_asos(session, time_from, time_to)

    def fetch_station(
        self,
        session: db.SessionDep,
    ) -> Sequence[db.Station]:
        # TODO: After implementing _read_station method, this method should call
        # _read_station first and catch exception to get station data from the
        # API. Currently this method always gets station data from the API.
        return self._get_station(session)

    def _get_station(self, session: db.SessionDep) -> Sequence[db.Station]:
        try:
            response = self._request_station()
        except requests.exceptions.Timeout, requests.exceptions.ConnectionError:
            return []
        rows = db.Station.from_strs(response.text.split("\n"))
        self._save_station(session, rows)
        return rows

    def _get_asos(
        self,
        session: db.SessionDep,
        time_from: int = 0,
        time_to: int = 0,
    ) -> Sequence[db.ASOS]:
        try:
            response = self._request_asos(time_from, time_to)
        except requests.exceptions.Timeout, requests.exceptions.ConnectionError:
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
        # TODO: Check whether ASOS data of given time range is exist in the DB
        # and return if exist else raise exception to get data from the API.
        raise NotImplementedError

    def _read_station(self, session: db.SessionDep) -> Sequence[db.Station]:
        # TODO: Check whether station data of given time range is exist in the
        # DB and return if exist else raise exception to get data from the API.
        raise NotImplementedError

    def _save_asos(self, session: db.SessionDep, rows: Sequence[db.ASOS]):
        for row in rows:
            if (
                session.exec(
                    sqlmodel.select(db.ASOS).where(
                        db.ASOS.timestamp == row.timestamp,
                        db.ASOS.station == row.station,
                    )
                ).first()
                is not None
            ):
                continue
            session.add(row)
            session.commit()

    def _save_station(self, session: db.SessionDep, rows: Sequence[db.Station]):
        for row in rows:
            if (
                session.exec(
                    sqlmodel.select(db.Station).where(
                        db.Station.id == row.id,
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
        # Possibly raise requests.exceptions.Timeout
        tm1 = self._KST_datetime_from_timestamp(time_from)
        tm2 = self._KST_datetime_from_timestamp(time_to)
        url = self.BASE_URL + "/url/kma_sfctm3.php"
        params = {
            "authKey": self.auth_key,
            "tm1": tm1.strftime("%Y%m%d%H00"),
            "tm2": tm2.strftime("%Y%m%d%H00"),
            "stn": 0,
        }
        return requests.get(url, params=params, timeout=1)

    def _request_station(self) -> requests.Response:
        url = self.BASE_URL + "/url/stn_inf.php"
        params = {
            "authKey": self.auth_key,
            "inf": "SFC",
        }
        return requests.get(url, params=params, timeout=1)

    def _KST_datetime_from_timestamp(self, timestamp: int) -> datetime.datetime:
        if timestamp <= 0:
            return datetime.datetime.now(self.KST_TIMEZONE)
        return datetime.datetime.fromtimestamp(timestamp, self.KST_TIMEZONE)
