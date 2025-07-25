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
    GoalValue: float
    CurrentValue: float
    user_id: int
    historico: List[Transaction]

    class Config:
        from_attributes = True
class GoalEditRequest(BaseModel):
    newName: str
    newGoal: float
