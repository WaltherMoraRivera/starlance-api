from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import mongodb
from app.routers import (
    task_router,
    balance_router,
    reward_router,
    family_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongodb.connect_to_mongo()
    yield
    await mongodb.close_mongo_connection()


app = FastAPI(
    title="StarLance API",
    description="A gamified task management system for families.",
    version="1.0.0",
    lifespan=lifespan,
)

# Include all the routers
app.include_router(family_router.router)
app.include_router(task_router.router)
app.include_router(reward_router.router)
app.include_router(balance_router.router)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the StarLance API!"}
