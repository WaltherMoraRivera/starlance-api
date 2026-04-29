from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional


def _doc_to_task(doc: dict) -> dict:
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


async def create_task(db, task_data: dict) -> dict:
    task_data = dict(task_data)
    task_data["completed"] = False
    task_data["created_at"] = datetime.now(timezone.utc)
    result = await db.tasks.insert_one(task_data)
    task_data["id"] = str(result.inserted_id)
    return task_data


async def get_task(db, task_id: str) -> Optional[dict]:
    doc = await db.tasks.find_one({"_id": ObjectId(task_id)})
    return _doc_to_task(doc) if doc else None


async def get_tasks(db) -> list:
    cursor = db.tasks.find()
    docs = await cursor.to_list(length=100)
    return [_doc_to_task(doc) for doc in docs]


async def update_task(db, task_id: str, update_data: dict) -> Optional[dict]:
    await db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data},
    )
    return await get_task(db, task_id)


async def delete_task(db, task_id: str) -> bool:
    result = await db.tasks.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count > 0
