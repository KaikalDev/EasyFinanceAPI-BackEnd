from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class ModelUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    categories = relationship("ModelCategory", back_populates="user", cascade="all, delete-orphan")
    historico = relationship("ModelTransaction", back_populates="user", cascade="all, delete-orphan")
    metas = relationship("ModelGoal", back_populates="user", cascade="all, delete-orphan")
    cofrinhos = relationship("ModelPiggybank", back_populates="user", cascade="all, delete-orphan")

class ModelCategory(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("ModelUser", back_populates="categories")

class ModelTransaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    category = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("ModelUser", back_populates="historico")

    cofrinho_id = Column(Integer, ForeignKey("piggybanks.id"), nullable=True)
    cofrinho = relationship("ModelPiggybank", back_populates="historico")

class ModelGoal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    goal_value = Column(Float, nullable=False)
    goal_date = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("ModelUser", back_populates="metas")

class ModelPiggybank(Base):
    __tablename__ = "piggybanks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    total = Column(Float, default=0.0)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("ModelUser", back_populates="cofrinhos")

    historico = relationship("ModelTransaction", back_populates="cofrinho", cascade="all, delete-orphan")
