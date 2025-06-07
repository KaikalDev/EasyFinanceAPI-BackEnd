from fastapi import APIRouter, Depends, HTTPException
from api.data.db import get_db
from api.services.CategoryService import CategoryService
from api.schemas.Category import Category, CategoryResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.auth import get_user_id_from_token

router = APIRouter()

@router.post("/add", response_model=CategoryResponse)
async def create(category: Category, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = CategoryService(db)
    return await service.create(category, userId)

@router.get("/getAll", response_model=list[CategoryResponse])
async def get_All(db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = CategoryService(db)
    return await service.getAll(userId)