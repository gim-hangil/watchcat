import contextlib
import fastapi
import logging
from . import db, api


logging.basicConfig(level=logging.INFO)


@contextlib.asynccontextmanager
async def lifespan(_: fastapi.FastAPI):
    db.create_db_and_tables()
    yield


app = fastapi.FastAPI(lifespan=lifespan)
app.frontend("/", directory="dist")
app.mount("/api", api.app)
