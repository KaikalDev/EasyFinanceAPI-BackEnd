from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from api.data.models.ModelCategory import ModelCategory
from api.data.models.ModelTransaction import ModelTransaction
from api.schemas.Category import Category
from api.schemas.Transaction import TransactionResponse

class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, category: Category, userId: int):
        try:
            db_category = ModelCategory(
                name=category.name,
                user_id=userId,
            )
            self.db.add(db_category)
            await self.db.commit()
            await self.db.refresh(db_category)
            return db_category
        except SQLAlchemyError:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Erro ao criar categoria")
    
    async def getAll(self, userId: int):
        try:
            stmt = select(ModelCategory).where(ModelCategory.user_id == userId)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Erro ao buscar categorias")
    
    async def getHistorico(self, categoryId: int, userId: int):
        try:
            category = await self.db.get(ModelCategory, categoryId)
            if not category:
                raise HTTPException(status_code=404, detail="Categoria não encontrada")

            if category.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado")

            query = (
                select(ModelTransaction)
                .options(selectinload(ModelTransaction.category))
                .where(ModelTransaction.category_id == categoryId)
            )
            result = await self.db.execute(query)
            historico = result.scalars().all()

            return [
                TransactionResponse(
                    id=t.id,
                    type=t.type,
                    value=t.value,
                    date=t.date,
                    category=t.category.name,
                    goal_id=t.goal_id
                )
                for t in historico
            ]
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Erro ao buscar histórico da categoria")
