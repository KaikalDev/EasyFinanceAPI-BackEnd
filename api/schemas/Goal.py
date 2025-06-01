from pydantic import BaseModel
from datetime import date

class Goal(BaseModel):
    name: str
    goal_value: float
    goal_date: date

    class Config:
        from_attributes = True

class GoalResponse(BaseModel):
    id: int
    name: str
    goal_value: float
    goal_date: date
    user_id: int

    class Config:
        from_attributes = True
