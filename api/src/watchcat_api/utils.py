import datetime
import sqlmodel
from collections.abc import Sequence
from . import db, kma


def fetchCurrentTemperature(session: db.SessionDep, station_id: int) -> float:
    currentASOS = fetchCurrentASOS(session, station_id)
    return currentASOS.temperature


def fetchCurrentRain(session: db.SessionDep, station_id: int) -> float:
    currentASOS = fetchCurrentASOS(session, station_id)
    return currentASOS.rainfall


def fetchCurrentPM10(session: db.SessionDep, station_id: int) -> int:
    kma.WeatherAPI().fetch_pm10(session, getCurrentTimestamp())
    currentPM10 = session.exec(
        sqlmodel.select(db.PM)
        .where(
            db.PM.station_id == station_id
            and db.PM.timestamp - getCurrentTimestamp() <= 30 * 60
        )
        .order_by(sqlmodel.col(db.PM.timestamp).desc())
    ).first()
    if currentPM10 is None:
        raise Exception("No ASOS data found for the given station_id and timestamp.")
    return currentPM10.pm10


def fetchCurrentASOS(session: db.SessionDep, station_id: int) -> db.ASOS:
    kma.WeatherAPI().fetch_asos(session, getCurrentTimestamp())
    currentASOS = session.exec(
        sqlmodel.select(db.ASOS)
        .where(
            db.ASOS.station_id == station_id
            and db.ASOS.timestamp - getCurrentTimestamp() <= 30 * 60
        )
        .order_by(sqlmodel.col(db.ASOS.timestamp).desc())
    ).first()
    if currentASOS is None:
        raise Exception("No ASOS data found for the given station_id and timestamp.")
    return currentASOS


def fetchStationData(session: db.SessionDep) -> Sequence[db.Station]:
    kma.WeatherAPI().fetch_station(session, getCurrentTimestamp())
    currentStations = session.exec(
        sqlmodel.select(db.Station)
        .where(db.Station.timestamp - getCurrentTimestamp() <= 12 * 60 * 60)
        .where(db.Station.timestamp - getCurrentTimestamp() >= -12 * 60 * 60)
    ).all()
    return currentStations


def getCurrentTimestamp() -> int:
    return int(datetime.datetime.now().timestamp())


def fetchAccidentType(session: db.SessionDep) -> Sequence[db.AccidentType]:
    accident_types = session.exec(sqlmodel.select(db.AccidentType)).all()
    return accident_types
