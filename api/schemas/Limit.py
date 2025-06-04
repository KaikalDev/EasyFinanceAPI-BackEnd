from pydantic import BaseModel
from datetime import date

class Limit(BaseModel):
    category: str
    value: float

    class Config:
        from_attributes = True

class LimitResponse(BaseModel):
    id: int
    category: str
    value: float
    user_id: int
    class Config:
        from_attributes = True
