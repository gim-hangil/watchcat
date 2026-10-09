import dotenv
import fastapi
import os
import re
import sqlmodel
import sqlalchemy.exc
from typing import Annotated, Sequence

dotenv.load_dotenv()
DB_URL = os.environ.get("DB_URL", "sqlite:///test.db")
connect_args = {"check_same_thread": False}
engine = sqlmodel.create_engine(DB_URL, connect_args=connect_args)


def get_session():
    with sqlmodel.Session(engine) as session:
        yield session


def create_db_and_tables():
    sqlmodel.SQLModel.metadata.create_all(engine)
    # FIXME: There should be a admin page to edit week data.
    # But for now, we just insert the week data here.
    try:
        with sqlmodel.Session(engine) as session:
            session.add_all(
                [
                    Week(id=1, label="자율적 부대운영"),
                    Week(id=2, label="훈련 준비"),
                    Week(id=3, label="전술훈련"),
                    Week(id=4, label="훈련 후 정비"),
                    Week(id=5, label="전투진지공사"),
                    Week(id=6, label="집중정신전력교육"),
                    Week(id=7, label="집중인성교육"),
                    Week(id=8, label="주특기 훈련"),
                ]
            )
            session.commit()
    except sqlalchemy.exc.IntegrityError:
        return


class ASOS(sqlmodel.SQLModel, table=True):
    timestamp: int = sqlmodel.Field(primary_key=True)
    station: int = sqlmodel.Field(primary_key=True)
    atmosphere: float
    wind_speed: float
    temperature: float
    humidity: float
    rainfall: float
    rainfall_day: float
    snowfall_3h: float
    snowfall_day: float

    @classmethod
    def from_str(cls, data: str) -> ASOS:
        items = data.split()
        return cls(
            timestamp=int(items[0]),
            station=int(items[1]),
            atmosphere=float(items[7]),
            wind_speed=float(items[3]),
            temperature=float(items[11]),
            humidity=float(items[13]),
            rainfall=float(items[15]),
            rainfall_day=float(items[16]),
            snowfall_3h=float(items[20]),
            snowfall_day=float(items[21]),
        )

    @classmethod
    def from_strs(cls, data: Sequence[str]) -> Sequence[ASOS]:
        data = [re.sub("#.*", "", line).strip() for line in data]
        data = [line for line in data if len(line) > 0]
        return [cls.from_str(line) for line in data]


class Station(sqlmodel.SQLModel, table=True):
    id: int = sqlmodel.Field(primary_key=True)
    location: str
    address: str

    @classmethod
    def from_str(cls, data: str) -> Station:
        items = data.split()
        return cls(
            id=int(items[0]),
            location=items[10],
            address=items[15],
        )

    @classmethod
    def from_strs(cls, data: Sequence[str]) -> Sequence[Station]:
        data = [re.sub("#.*", "", line).strip() for line in data]
        data = [line for line in data if len(line) > 0]
        return [cls.from_str(line) for line in data]


class AccidentType(sqlmodel.SQLModel, table=True):
    id: int = sqlmodel.Field(primary_key=True, default=None)
    label: str


class Accident(sqlmodel.SQLModel, table=True):
    id: int = sqlmodel.Field(primary_key=True, default=None)
    week_id: int = sqlmodel.Field(foreign_key="week.id")
    type_id: int = sqlmodel.Field(foreign_key="accidenttype.id")
    timestamp: int
    station: int


class Week(sqlmodel.SQLModel, table=True):
    id: int = sqlmodel.Field(primary_key=True)
    label: str


SessionDep = Annotated[sqlmodel.Session, fastapi.Depends(get_session)]
