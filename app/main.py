from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import mongodb
from app.routers import task_router, balance_router, reward_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongodb.connect_to_mongo()
    yield
    await mongodb.close_mongo_connection()


app = FastAPI(title="StarLance API", lifespan=lifespan)

app.include_router(task_router.router, prefix="/tasks", tags=["tasks"])
app.include_router(balance_router.router, prefix="/balance", tags=["balance"])
app.include_router(reward_router.router, prefix="/rewards", tags=["rewards"])


@app.get("/")
async def root():
    return {"message": "StarLance API"}
