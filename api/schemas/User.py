from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    password: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    password: str
    email: EmailStr
