from pydantic import BaseModel
from typing import List
from api.schemas.Transaction import Transaction

class Goal(BaseModel):
    name: str
    GoalValue: float
    CurrentValue: float

    class Config:
        from_attributes = True

class GoalResponse(BaseModel):
    id: int
    name: str
    total: float
    user_id: int
    historico: list[Transaction]

    class Config:
        from_attributes = True