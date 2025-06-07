from pydantic import BaseModel
from datetime import date

class Category(BaseModel):
    name: str

    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True
