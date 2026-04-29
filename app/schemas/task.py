from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    approved = "approved"


class TaskType(str, Enum):
    daily = "daily"
    weekly = "weekly"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    points: int
    assigned_to_id: str
    family_id: str
    task_type: TaskType


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    points: Optional[int] = None
    status: Optional[TaskStatus] = None


class TaskResponse(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    description: Optional[str] = None
    points: int
    assigned_to_id: str
    family_id: str
    status: TaskStatus = TaskStatus.pending
    task_type: TaskType
    created_at: datetime
