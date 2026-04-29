from fastapi import APIRouter, Depends
from app.db.mongodb import get_db
from app.schemas.transaction import BalanceResponse, TransactionResponse
from app.services import balance_service
from typing import List

router = APIRouter()


@router.get("/{member_id}", response_model=BalanceResponse)
async def get_balance(member_id: str, db=Depends(get_db)):
    return await balance_service.get_balance(db, member_id)


@router.get("/{member_id}/transactions", response_model=List[TransactionResponse])
async def get_transactions(member_id: str, db=Depends(get_db)):
    return await balance_service.get_transactions(db, member_id)
