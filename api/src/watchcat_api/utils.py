import datetime
import sqlalchemy.exc
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


def fetch_safety_tips(session: db.SessionDep, accident_id: int) -> Sequence[db.SafetyTip]:
    try:
        tips = session.exec(sqlmodel.select(db.SafetyTip).where(db.SafetyTip.accident_id == accident_id)).all()
    except:
        return []
    return tips


def insert_default_data(engine: sqlalchemy.engine.base.Engine):
    insert_default_weeks(engine)
    insert_default_accident_types(engine)
    insert_default_tips(engine)


def insert_default_weeks(engine: sqlalchemy.engine.base.Engine):
    try:
        with sqlmodel.Session(engine) as session:
            session.add_all(
                [
                    db.Week(id=1, label="자율적 부대운영"),
                    db.Week(id=2, label="훈련 준비"),
                    db.Week(id=3, label="전술훈련"),
                    db.Week(id=4, label="훈련 후 정비"),
                    db.Week(id=5, label="전투진지공사"),
                    db.Week(id=6, label="집중정신전력교육"),
                    db.Week(id=7, label="집중인성교육"),
                    db.Week(id=8, label="주특기 훈련"),
                ]
            )
            session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


def insert_default_accident_types(engine: sqlalchemy.engine.base.Engine):
    try:
        with sqlmodel.Session(engine) as session:
            session.add_all(
                [
                    db.AccidentType(id=1, label="식중독"),
                    db.AccidentType(id=2, label="온열손상"),
                    db.AccidentType(id=3, label="낙상"),
                    db.AccidentType(id=4, label="화재"),
                    db.AccidentType(id=5, label="교통사고"),
                ]
            )
            session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


def insert_default_tips(engine: sqlalchemy.engine.base.Engine):
    try:
        with sqlmodel.Session(engine) as session:
            session.add_all(
                [
                    db.SafetyTip(
                        id=1,
                        accident_id=1,
                        tip="급양감독 간 식사 전 손씻기, 보존식 유지 상태, 칼 및 도마 구분 사용을 잘 확인해주세요.",
                    ),
                    db.SafetyTip(
                        id=2,
                        accident_id=1,
                        tip="식중독 발생 시 이온음료를 조금씩 섭취시키고, 증상이 급성으로 나타난다면 금식 조치해주세요.",
                    ),
                    db.SafetyTip(
                        id=3,
                        accident_id=2,
                        tip="야외 활동 간 반드시 온열손상키트와 폭염응급키트를 휴대하고, 적어도 50분마다 10분 이상 휴식을 부여해주세요.",
                    ),
                    db.SafetyTip(
                        id=4,
                        accident_id=2,
                        tip="온열손상 발생 시 환자를 그늘로 이동시키고 체온을 낮추어주세요.",
                    ),
                    db.SafetyTip(
                        id=5,
                        accident_id=2,
                        tip="온열손상 발생 시 환자에게 의식이 있는 경우에만 물을 섭취시켜야 합니다.",
                    ),
                    db.SafetyTip(
                        id=6,
                        accident_id=3,
                        tip="낙상사고 발생 시 환자의 의식 여부를 확인하고, 2차 손상을 예방하기 위해 이동시키지 말고 안정시켜주세요.",
                    ),
                    db.SafetyTip(
                        id=7,
                        accident_id=3,
                        tip="과업 수행 전 안전장구류를 전원 착용하였는지 반드시 확인하고, 중간에 벗는 인원이 없도록 신경써주세요.",
                    ),
                    db.SafetyTip(
                        id=8,
                        accident_id=4,
                        tip="인화성 물질로 작업하는 경우 작업장 주변에 소화기를 비치하고, 작업 전 안전교육을 실시해주세요.",
                    ),
                    db.SafetyTip(
                        id=9,
                        accident_id=4,
                        tip="화재 발생 시 즉시 지휘관에게 보고하고, 2차 피해를 예방하기 위해 임의로 소방대를 투입하는 것이 아닌 신속한 대피를 통제해주세요.",
                    ),
                    db.SafetyTip(
                        id=10,
                        accident_id=5,
                        tip="차량 운행 전 반드시 차량 점검을 실시하고, 운행자의 졸음 방지를 위한 졸음껌과 감미품 등을 준비해주세요.",
                    ),
                    db.SafetyTip(
                        id=11,
                        accident_id=5,
                        tip="장거리 운행 시 반드시 휴게소에서 휴식을 취하고, 가능할 경우 운전자를 교대해주세요.",
                    ),
                ]
            )
            session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass
