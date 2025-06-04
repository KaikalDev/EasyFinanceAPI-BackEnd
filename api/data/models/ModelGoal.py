from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey
)
from sqlalchemy.orm import relationship
from api.data.db import Base

class ModelGoal(Base):
    __tablename__ = "goal"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    GoalValue = Column(Float, default=0.0)
    CurrentValue = Column(Float, default=0.0)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("ModelUser", back_populates="goals")

    historico = relationship("ModelTransaction", back_populates="goal", cascade="all, delete-orphan")
