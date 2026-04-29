from bson import ObjectId
from datetime import datetime, timezone


def _doc_to_transaction(doc: dict) -> dict:
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


async def create_transaction(db, transaction_data: dict) -> dict:
    transaction_data = dict(transaction_data)
    transaction_data["created_at"] = datetime.now(timezone.utc)
    result = await db.transactions.insert_one(transaction_data)
    transaction_data["id"] = str(result.inserted_id)
    return transaction_data


async def get_transactions_by_member(db, member_id: str) -> list:
    cursor = db.transactions.find({"member_id": member_id})
    docs = await cursor.to_list(length=1000)
    return [_doc_to_transaction(doc) for doc in docs]
