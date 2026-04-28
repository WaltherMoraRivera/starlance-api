from fastapi import HTTPException
from app.repositories import task_repository, transaction_repository
from app.schemas.task import TaskCreate, TaskUpdate


async def create_task(db, task_data: TaskCreate) -> dict:
    return await task_repository.create_task(db, task_data.model_dump())


async def get_tasks(db) -> list:
    return await task_repository.get_tasks(db)


async def get_task(db, task_id: str) -> dict:
    task = await task_repository.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def update_task(db, task_id: str, update_data: TaskUpdate) -> dict:
    data = update_data.model_dump(exclude_none=True)
    task = await task_repository.update_task(db, task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def complete_task(db, task_id: str) -> dict:
    task = await task_repository.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.get("completed"):
        raise HTTPException(status_code=400, detail="Task already completed")

    updated_task = await task_repository.update_task(db, task_id, {"completed": True})

    await transaction_repository.create_transaction(db, {
        "member_id": task["assigned_to"],
        "points": task["points"],
        "type": "earned",
        "reference_id": task_id,
    })

    return updated_task
