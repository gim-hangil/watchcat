import datetime
import sqlmodel
import fastapi
import fastapi.responses
from typing import Annotated
from . import db

app = fastapi.FastAPI()


@app.post("/accident")
def add_accident(
    session: db.SessionDep,
    week_id: Annotated[int, fastapi.Form()],
    timestamp: Annotated[str, fastapi.Form()],
    station: Annotated[int, fastapi.Form()],
    another_accident: Annotated[str | None, fastapi.Form()] = None,
    accident_id: Annotated[int | None, fastapi.Form()] = None,
):
    if another_accident is not None and another_accident != "":
        session.add(db.AccidentType(label=another_accident))
        session.commit()
        accident = session.exec(
            sqlmodel.select(db.AccidentType).where(
                db.AccidentType.label == another_accident
            )
        ).first()
        if accident is not None:
            accident_id = accident.id
        else:
            return fastapi.responses.RedirectResponse(
                url="/",
                status_code=fastapi.status.HTTP_406_NOT_ACCEPTABLE,
            )
    if accident_id is None:
        return fastapi.responses.RedirectResponse(
            url="/",
            status_code=fastapi.status.HTTP_406_NOT_ACCEPTABLE,
        )
    session.add(
        db.Accident(
            type_id=accident_id,
            week_id=week_id,
            timestamp=datetime.datetime.fromisoformat(timestamp).timestamp(),
            station=station,
        )
    )
    session.commit()
    return fastapi.responses.RedirectResponse(
        url="/", status_code=fastapi.status.HTTP_302_FOUND
    )
