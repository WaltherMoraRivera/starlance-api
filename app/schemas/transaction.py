from pydantic import BaseModel
from datetime import datetime


class TransactionCreate(BaseModel):
    member_id: str
    points: int
    type: str
    reference_id: str


class TransactionResponse(BaseModel):
    id: str
    member_id: str
    points: int
    type: str
    reference_id: str
    created_at: datetime


class BalanceResponse(BaseModel):
    member_id: str
    balance: int
