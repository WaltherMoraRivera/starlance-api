from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional


def _doc_to_member(doc: dict) -> dict:
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


async def create_member(db, member_data: dict) -> dict:
    member_data = dict(member_data)
    member_data["created_at"] = datetime.now(timezone.utc)
    result = await db.members.insert_one(member_data)
    member_data["id"] = str(result.inserted_id)
    return member_data


async def get_member(db, member_id: str) -> Optional[dict]:
    doc = await db.members.find_one({"_id": ObjectId(member_id)})
    return _doc_to_member(doc) if doc else None


async def get_members(db) -> list:
    cursor = db.members.find()
    docs = await cursor.to_list(length=100)
    return [_doc_to_member(doc) for doc in docs]
