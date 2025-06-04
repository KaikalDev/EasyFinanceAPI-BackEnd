from sqlalchemy import (
    Column, Integer, String
)
from sqlalchemy.orm import relationship
from api.data.db import Base

class ModelUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    categories = relationship("ModelCategory", back_populates="user", cascade="all, delete-orphan")
    historical = relationship("ModelTransaction", back_populates="user", cascade="all, delete-orphan")
    limit = relationship("ModelLimit", back_populates="user", cascade="all, delete-orphan")
    goal = relationship("ModelGoal", back_populates="user", cascade="all, delete-orphan")
