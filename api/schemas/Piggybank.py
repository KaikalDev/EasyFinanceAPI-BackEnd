from pydantic import BaseModel
from typing import List
from api.schemas.Transaction import Transaction

class Piggybank(BaseModel):
    name: str

    class Config:
        from_attributes = True

class PiggybankResponse(BaseModel):
    id: int
    name: str
    total: float

    class Config:
        from_attributes = True