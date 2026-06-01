from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_dt: datetime
    end_dt: datetime


class TaskModelResponse(TaskCreate):
    id: int
    state: str
    user_id: int
    real_start_dt: Optional[datetime]
    real_end_dt: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TaskDateTimeFilter(BaseModel):
    by_date: Optional[date] = None
    start_dt: Optional[datetime] = None
    end_dt: Optional[datetime] = None
