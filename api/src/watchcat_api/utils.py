import datetime
import sqlmodel
from collections.abc import Sequence
from . import db, kma


def fetch_current_temperature(session: db.SessionDep, station_id: int) -> float:
    currentASOS = fetch_current_asos(session, station_id)
    return currentASOS.temperature


def fetch_current_rain(session: db.SessionDep, station_id: int) -> float:
    currentASOS = fetch_current_asos(session, station_id)
    return currentASOS.rainfall


def fetch_current_pm10(session: db.SessionDep, station_id: int) -> int:
    kma.WeatherAPI().fetch_pm10(session, fetch_current_timestamp())
    try:
        currentPM10 = session.exec(
            sqlmodel.select(db.PM)
            .where(
                db.PM.station_id == station_id
                and db.PM.timestamp - fetch_current_timestamp() <= 30 * 60
            )
            .order_by(sqlmodel.col(db.PM.timestamp).desc())
        ).one()
    except:
        raise Exception("No ASOS data found for the given station_id and timestamp.")
    return currentPM10.pm10


def fetch_current_asos(session: db.SessionDep, station_id: int) -> db.ASOS:
    kma.WeatherAPI().fetch_asos(session, fetch_current_timestamp())
    try:
        currentASOS = session.exec(
            sqlmodel.select(db.ASOS)
            .where(
                db.ASOS.station_id == station_id
                and db.ASOS.timestamp - fetch_current_timestamp() <= 30 * 60
            )
            .order_by(sqlmodel.col(db.ASOS.timestamp).desc())
        ).one()
    except:
        raise Exception("No ASOS data found for the given station_id and timestamp.")
    return currentASOS


def fetch_current_station(session: db.SessionDep) -> Sequence[db.Station]:
    kma.WeatherAPI().fetch_station(session, fetch_current_timestamp())
    currentStations = session.exec(
        sqlmodel.select(db.Station)
        .where(db.Station.timestamp - fetch_current_timestamp() <= 12 * 60 * 60)
        .where(db.Station.timestamp - fetch_current_timestamp() >= -12 * 60 * 60)
    ).all()
    return currentStations


def fetch_current_timestamp() -> int:
    return int(datetime.datetime.now().timestamp())


def fetch_accident_type(session: db.SessionDep) -> Sequence[db.AccidentType]:
    accident_types = session.exec(sqlmodel.select(db.AccidentType)).all()
    return accident_types
