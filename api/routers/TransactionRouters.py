from fastapi import APIRouter, Depends, HTTPException
from api.data.db import get_db
from api.services.TransactionService import TransactionService
from api.schemas.Transaction import Transaction, TransactionResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.auth import get_user_id_from_token

router = APIRouter()

@router.post("/add", response_model=TransactionResponse)
async def create(tran: Transaction, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = TransactionService(db)
    return await service.create(tran, userId)

@router.get("/get/{id}", response_model=TransactionResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = TransactionService(db)
    return await service.getById(id, userId)

@router.delete("/delete/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = TransactionService(db)
    return await service.delete(id, userId)

@router.put("/edit/{id}", response_model=TransactionResponse)
async def edit(id: int,tran: Transaction, db: AsyncSession = Depends(get_db), userId: int = Depends(get_user_id_from_token)):
    service = TransactionService(db)
    return await service.edit(id, tran, userId)
