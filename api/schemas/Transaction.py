from pydantic import BaseModel
from datetime import date
from typing import Optional

class Transaction(BaseModel):
    type: str
    value: float
    date: date
    category: str
    goal_id: Optional[int] = None

class TransactionResponse(BaseModel):
    id: int
    type: str
    value: float
    date: date
    category: str
    goal_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }
