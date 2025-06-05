from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from api.data.db import Base

class ModelTransaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    category = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("ModelUser", back_populates="historical")

    goal_id = Column(Integer, ForeignKey("goal.id"), nullable=True)
    goal = relationship("ModelGoal", back_populates="historico")