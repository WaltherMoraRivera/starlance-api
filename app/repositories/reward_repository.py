from bson import ObjectId
from typing import Optional


def _doc_to_reward(doc: dict) -> dict:
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


async def create_reward(db, reward_data: dict) -> dict:
    reward_data = dict(reward_data)
    result = await db.rewards.insert_one(reward_data)
    reward_data["id"] = str(result.inserted_id)
    return reward_data


async def get_reward(db, reward_id: str) -> Optional[dict]:
    doc = await db.rewards.find_one({"_id": ObjectId(reward_id)})
    return _doc_to_reward(doc) if doc else None


async def get_rewards(db) -> list:
    cursor = db.rewards.find()
    docs = await cursor.to_list(length=100)
    return [_doc_to_reward(doc) for doc in docs]
