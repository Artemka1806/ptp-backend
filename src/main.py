from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.models import ALL_DB_MODELS
from src.routers import ALL_ROUTERS
from src.utils import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(ALL_DB_MODELS)
    yield

app = FastAPI(title="Pet The Plant API", lifespan=lifespan)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

for router in ALL_ROUTERS:
    app.include_router(router)


@app.get("/", include_in_schema=False)
async def read_root():
    return "Hello, world!"
