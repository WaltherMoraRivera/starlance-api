from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    points: int
    assigned_to: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    points: Optional[int] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    points: int
    assigned_to: str
    completed: bool = False
    created_at: datetime
