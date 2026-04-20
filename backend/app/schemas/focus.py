from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class FocusType(str, Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"

class FocusSessionCreate(BaseModel):
    focus_type: FocusType = FocusType.WORK
    duration_minutes: int = 25

class FocusSessionOut(BaseModel):
    id: int
    focus_type: FocusType
    duration_minutes: int
    completed: bool
    started_at: datetime
    ended_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class FocusComplete(BaseModel):
    session_id: int
    completed: bool

class DailyStatsOut(BaseModel):
    date: datetime
    focus_minutes: int
    sessions_completed: int
    
    class Config:
        from_attributes = True
