from fastapi import APIRouter, Depends, HTTPException
from api.data.db import get_db
from api.services.LimitService import LimitService
from api.schemas.Limit import Limit, LimitResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.auth import get_user_id_from_token

router = APIRouter()

@router.post("/add", response_model=LimitResponse)
async def create(limit: Limit, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = LimitService(db)
    return await service.create(limit, userId)

@router.get("/get/{id}", response_model=LimitResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = LimitService(db)
    return await service.getById(id, userId)

@router.delete("/delete/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = LimitService(db)
    return await service.delete(id, userId)

@router.put("/edit/{id}", response_model=LimitResponse)
async def edit(id: int, newLimit: Limit, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = LimitService(db)
    return await service.edit(id, newLimit, userId)

@router.get("/getAll", response_model=list[LimitResponse])
async def get_All(db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = LimitService(db)
    return await service.getAll(userId)