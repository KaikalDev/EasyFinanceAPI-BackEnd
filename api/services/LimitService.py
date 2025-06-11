from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from api.data.models.ModelLimit import ModelLimit

class LimitService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, limit: ModelLimit, userId: int):
        try:
            db_limit = ModelLimit(
                category=limit.category,
                value=limit.value,
                user_id=userId,
            )
            self.db.add(db_limit)
            await self.db.commit()
            await self.db.refresh(db_limit)
            return db_limit
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao criar limite: {str(e)}")

    async def edit(self, id: int, newLimit: ModelLimit, userId: int):
        try:
            limit = await self.db.get(ModelLimit, id)
            if not limit:
                raise HTTPException(status_code=404, detail="Limite não encontrado")
            if limit.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado")

            limit.value = newLimit.value
            limit.category = newLimit.category

            await self.db.commit()
            await self.db.refresh(limit)
            return limit
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao editar limite: {str(e)}")

    async def delete(self, id: int, userId: int):
        try:
            limit = await self.db.get(ModelLimit, id)
            if not limit:
                raise HTTPException(status_code=404, detail="Limite não encontrado")
            if limit.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado")

            await self.db.delete(limit)
            await self.db.commit()
            return {"detail": "Limite deletado"}
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao deletar limite: {str(e)}")

    async def getById(self, id: int, userId: int):
        try:
            limit = await self.db.get(ModelLimit, id)
            if not limit:
                raise HTTPException(status_code=404, detail="Limite não encontrado")
            if limit.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado")
            return limit
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar limite: {str(e)}")

    async def getAll(self, userId: int):
        try:
            stmt = select(ModelLimit).where(ModelLimit.user_id == userId)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar limites: {str(e)}")
