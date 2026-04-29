from fastapi import APIRouter, Depends
from app.db.mongodb import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service
from typing import List

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate, db=Depends(get_db)):
    return await task_service.create_task(db, task)


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(db=Depends(get_db)):
    return await task_service.get_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, db=Depends(get_db)):
    return await task_service.get_task(db, task_id)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task: TaskUpdate, db=Depends(get_db)):
    return await task_service.update_task(db, task_id, task)


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: str, db=Depends(get_db)):
    return await task_service.complete_task(db, task_id)
