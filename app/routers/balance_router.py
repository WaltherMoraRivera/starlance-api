from fastapi import APIRouter, status
from typing import List
from app.schemas.transaction import BalanceResponse, TransactionResponse
from app.services import balance_service

router = APIRouter(tags=["Balance & Transactions"])


@router.get("/balance/{user_id}", response_model=BalanceResponse)
async def get_balance(user_id: str):
    return await balance_service.get_total_balance_service(user_id)


@router.get("/transactions/{user_id}", response_model=List[TransactionResponse])
async def get_transactions(user_id: str):
    return await balance_service.get_transactions_service(user_id)
