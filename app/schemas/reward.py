from pydantic import BaseModel
from typing import Optional


class RewardCreate(BaseModel):
    name: str
    description: Optional[str] = None
    cost: int


class RewardResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    cost: int
