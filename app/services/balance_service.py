from app.repositories import transaction_repository


async def get_balance(db, member_id: str) -> dict:
    transactions = await transaction_repository.get_transactions_by_member(db, member_id)
    balance = sum(
        t["points"] if t["type"] == "earned" else -t["points"]
        for t in transactions
    )
    return {"member_id": member_id, "balance": balance}


async def get_transactions(db, member_id: str) -> list:
    return await transaction_repository.get_transactions_by_member(db, member_id)
