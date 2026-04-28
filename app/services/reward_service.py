from fastapi import HTTPException
from app.repositories import reward_repository, transaction_repository
from app.schemas.reward import RewardCreate


async def create_reward(db, reward_data: RewardCreate) -> dict:
    return await reward_repository.create_reward(db, reward_data.model_dump())


async def get_rewards(db) -> list:
    return await reward_repository.get_rewards(db)


async def redeem_reward(db, member_id: str, reward_id: str) -> dict:
    reward = await reward_repository.get_reward(db, reward_id)
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")

    transactions = await transaction_repository.get_transactions_by_member(db, member_id)
    balance = sum(
        t["points"] if t["type"] == "earned" else -t["points"]
        for t in transactions
    )

    if balance < reward["cost"]:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    transaction = await transaction_repository.create_transaction(db, {
        "member_id": member_id,
        "points": reward["cost"],
        "type": "spent",
        "reference_id": reward_id,
    })

    return {"reward": reward, "transaction": transaction}
