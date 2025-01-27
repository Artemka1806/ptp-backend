from contextlib import asynccontextmanager

from fastapi import FastAPI

from .models import ALL_DB_MODELS
from .routers import ALL_ROUTERS
from .utils import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(ALL_DB_MODELS)
    yield

app = FastAPI(title="Pet The Plant API", lifespan=lifespan)

for router in ALL_ROUTERS:
    app.include_router(router)


@app.get("/", include_in_schema=False)
async def read_root():
    return "Hello, world!"
