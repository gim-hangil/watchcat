import fastapi
import fastapi.responses
import pydantic
import sqlalchemy.exc
import sqlmodel
from collections.abc import Sequence
from . import db, utils

app = fastapi.FastAPI()


DANGER_FACTOR = 1.5


class SafetyLevel(pydantic.BaseModel):
    job: str = ""
    level: int


@app.get("/level/{station_id}")
def get_current_safety_level(session: db.SessionDep, week_id: int = 0) -> SafetyLevel:
    TERM = 365 * 24 * 60 * 60
    total_accidents = len(
        session.exec(
            sqlmodel.select(db.Accident).where(
                db.Accident.timestamp > utils.fetch_current_timestamp() - TERM,
            )
        ).all()
    )
    possible_accidents = len(
        session.exec(
            sqlmodel.select(db.Accident).where(
                db.Accident.timestamp > utils.fetch_current_timestamp() - TERM,
                db.Accident.week_id == week_id,
            )
        ).all()
    )
    types_of_weeks = len(session.exec(sqlmodel.select(db.Week)).all())
    if total_accidents > 0:
        probability = possible_accidents * types_of_weeks / total_accidents
        return SafetyLevel(
            level=0 if probability < 1 else 1 if probability < DANGER_FACTOR else 2
        )
    else:
        return SafetyLevel(level=0)


@app.get("/level/{station_id}/temperature")
def get_current_temperature_level(
    session: db.SessionDep, station_id: int
) -> SafetyLevel:
    try:
        temperature = utils.fetch_current_temperature(session, station_id)
        return SafetyLevel(
            level=0 if temperature < 30 else 1 if temperature < 34 else 2
        )
    except Exception:
        return SafetyLevel(level=0)


@app.get("/level/{station_id}/rain")
def get_current_rain_level(session: db.SessionDep, station_id: int) -> SafetyLevel:
    try:
        rain = utils.fetch_current_rain(session, station_id)
        return SafetyLevel(level=0 if rain < 10 else 1 if rain < 20 else 2)
    except Exception:
        return SafetyLevel(level=0)


@app.get("/level/{station_id}/air")
def get_current_air_level(session: db.SessionDep, station_id: int) -> SafetyLevel:
    try:
        pm10 = utils.fetch_current_pm10(session, station_id)
        return SafetyLevel(level=0 if pm10 < 30 else 1 if pm10 < 80 else 2)
    except Exception:
        return SafetyLevel(level=0)


@app.get("/risk")
def get_current_most_risks(
    session: db.SessionDep, week_id: int = 0
) -> Sequence[SafetyLevel]:
    week_count = len(session.exec(sqlmodel.select(db.Week)).all())
    accident_types = session.exec(sqlmodel.select(db.AccidentType)).all()
    risks = []
    for accident_type in accident_types:
        accident_count = len(
            session.exec(
                sqlmodel.select(db.Accident).where(
                    db.Accident.type_id == accident_type.id,
                    db.Accident.week_id == week_id,
                )
            ).all()
        )
        total_count = len(
            session.exec(
                sqlmodel.select(db.Accident).where(
                    db.Accident.type_id == accident_type.id,
                )
            ).all()
        )
        if total_count > 0:
            probability = accident_count * week_count // total_count
        else:
            probability = 0
        risks.append(
            SafetyLevel(
                job=accident_type.label,
                level=0 if probability < 1 else 1 if probability < DANGER_FACTOR else 2,
            )
        )
    risks.sort(key=lambda risk: -risk.level)
    return risks[:5]


@app.get("/week")
def get_week_data(session: db.SessionDep) -> Sequence[db.Week]:
    week_data = session.exec(sqlmodel.select(db.Week)).all()
    return week_data


@app.get("/station")
def get_station_data(session: db.SessionDep) -> Sequence[db.Station]:
    station_data = utils.fetch_current_station(session)
    return station_data


@app.get("/tip")
def get_tips(session: db.SessionDep) -> list[str]:
    return ["준비 중...", "오늘의 안전사고 예방을 위한 팁을 알려드립니다."]


@app.get("/accident")
def get_accident_types(session: db.SessionDep) -> Sequence[db.AccidentType]:
    accident_type_data = utils.fetch_accident_type(session)
    return accident_type_data


@app.get("/forecast")
def get_weekly_forecast(session: db.SessionDep, week_id: int) -> SafetyLevel:
    TERM = 365 * 24 * 60 * 60
    try:
        currentWeekLabel = (
            session.exec(sqlmodel.select(db.Week).where(db.Week.id == week_id))
            .one()
            .label
        )
    except sqlalchemy.exc.NoResultFound:
        return SafetyLevel(job="", level=0)
    total_accidents = len(
        session.exec(
            sqlmodel.select(db.Accident).where(
                db.Accident.timestamp < utils.fetch_current_timestamp(),
                db.Accident.timestamp > utils.fetch_current_timestamp() - TERM,
            )
        ).all()
    )
    possible_accidents = len(
        session.exec(
            sqlmodel.select(db.Accident).where(
                db.Accident.timestamp < utils.fetch_current_timestamp(),
                db.Accident.timestamp > utils.fetch_current_timestamp() - TERM,
                db.Accident.week_id == week_id,
            )
        ).all()
    )
    types_of_weeks = len(session.exec(sqlmodel.select(db.Week)).all())

    if total_accidents > 0:
        probability = possible_accidents * types_of_weeks / total_accidents
        return SafetyLevel(
            job=currentWeekLabel,
            level=0 if probability < 1 else 1 if probability < DANGER_FACTOR else 2,
        )
    else:
        return SafetyLevel(job=currentWeekLabel, level=0)


@app.post("/accident")
def add_accident(
    session: db.SessionDep, accident: db.Accident
) -> fastapi.responses.RedirectResponse:
    try:
        session.add(accident)
        session.commit()
    except Exception:
        session.rollback()
        return fastapi.responses.RedirectResponse(
            url="/",
            status_code=fastapi.status.HTTP_409_CONFLICT,
        )
    return fastapi.responses.RedirectResponse(
        url="/",
        status_code=fastapi.status.HTTP_201_CREATED,
    )
