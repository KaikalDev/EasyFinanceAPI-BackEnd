from fastapi import APIRouter, Depends, HTTPException
from api.data.db import get_db
from api.services.CategoryService import CategoryService
from api.schemas.Category import Category, CategoryResponse
from api.schemas.Transaction import Transaction
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.auth import get_user_id_from_token

router = APIRouter()

@router.post("/add", response_model=CategoryResponse)
async def create(category: Category, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = CategoryService(db)
    try:
        return await service.create(category, userId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/getAll", response_model=list[CategoryResponse])
async def get_all(db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = CategoryService(db)
    return await service.getAll(userId)

@router.get("/{id}/historico", response_model=list[Transaction])
async def get_historico(id: int, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = CategoryService(db)
    return await service.getHistorico(id, userId)