from fastapi import APIRouter, Depends, HTTPException
from api.data.db import get_db
from api.services.GoalService import GoalService
from api.schemas.Goal import Goal, GoalResponse
from api.schemas.Transaction import Transaction
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.auth import get_user_id_from_token

router = APIRouter()

@router.post("/add", response_model=GoalResponse)
async def create(goal: Goal, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = GoalService(db)
    return await service.create(goal, userId)

@router.get("/get/{id}", response_model=GoalResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = GoalService(db)
    return await service.getById(id, userId)

@router.delete("/delete/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = GoalService(db)
    return await service.delete(id, userId)

@router.put("/edit/{id}", response_model=GoalResponse)
async def edit_name(id: int,newName: str, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = GoalService(db)
    return await service.editName(id, newName, userId)

@router.get("/{id}/historico", response_model=list[Transaction])
async def get_historico(id: int, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = GoalService(db)
    return await service.getHistorico(id, userId)

@router.get("/getAll", response_model=list[GoalResponse])
async def get_All(db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = GoalService(db)
    return await service.getAll(userId)
