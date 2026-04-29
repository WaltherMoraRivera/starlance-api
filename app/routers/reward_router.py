from fastapi import APIRouter, Depends
from app.db.mongodb import get_db
from app.schemas.reward import RewardCreate, RewardResponse
from app.services import reward_service
from typing import List

router = APIRouter()


@router.post("/", response_model=RewardResponse, status_code=201)
async def create_reward(reward: RewardCreate, db=Depends(get_db)):
    return await reward_service.create_reward(db, reward)


@router.get("/", response_model=List[RewardResponse])
async def get_rewards(db=Depends(get_db)):
    return await reward_service.get_rewards(db)


@router.post("/{reward_id}/redeem/{member_id}", response_model=dict)
async def redeem_reward(reward_id: str, member_id: str, db=Depends(get_db)):
    return await reward_service.redeem_reward(db, member_id, reward_id)
