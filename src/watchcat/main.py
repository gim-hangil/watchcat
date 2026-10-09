import contextlib
import fastapi
import sqlmodel
from fastapi import templating, responses, staticfiles
from . import db, kma, api, utils


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    db.create_db_and_tables()
    yield


templates = templating.Jinja2Templates(directory="templates")

app = fastapi.FastAPI(lifespan=lifespan)

app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")


@app.get("/", response_class=responses.HTMLResponse)
async def main(request: fastapi.Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context=utils.get_today()
    )


@app.get("/details", response_class=responses.Response)
async def details(request: fastapi.Request):
    return templates.TemplateResponse(
        request=request, name="details.html", context=utils.get_details()
    )


@app.get("/forecast", response_class=responses.Response)
async def forecast(request: fastapi.Request):
    return templates.TemplateResponse(
        request=request, name="forecast.html", context=utils.get_forecast()
    )


@app.get("/accident", response_class=responses.Response)
async def accident(session: db.SessionDep, request: fastapi.Request):
    api = kma.WeatherAPI()
    api.fetch_station(session)
    return templates.TemplateResponse(
        request=request,
        name="accident.html",
        context={
            "weeks": session.exec(sqlmodel.select(db.Week)).all(),
            "stations": session.exec(sqlmodel.select(db.Station)).all(),
            "accidents": session.exec(
                sqlmodel.select(db.AccidentType)
            ).all(),  # accident id and label pairs
        },
    )

@app.get("/config", response_class=responses.Response)
async def config(session: db.SessionDep, request: fastapi.Request):
    return templates.TemplateResponse(
        request=request,
        name="config.html",
        context={
            "weeks": session.exec(sqlmodel.select(db.Week)).all(),
        }
    )


app.mount("/api", api.app)
