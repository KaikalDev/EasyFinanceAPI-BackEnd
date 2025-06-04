from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey
)
from sqlalchemy.orm import relationship
from api.data.db import Base

class ModelLimit(Base):
    __tablename__ = "limits"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    category = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("ModelUser", back_populates="limit")