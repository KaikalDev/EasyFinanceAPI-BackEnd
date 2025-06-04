from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.data.models.ModelLimit import ModelLimit

class LimitService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, limit: ModelLimit, userId: int):
        db_limit = ModelLimit(
            goal_date=limit.category,
            goal_value=limit.value,
            user_id=userId,
        )
        self.db.add(db_limit)
        await self.db.commit()
        await self.db.refresh(db_limit)
        return db_limit

    async def edit(self, id: int, newLimit: ModelLimit, userId: int):
        limit = await self.db.get(ModelLimit, id)
        if not limit:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        if limit.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        limit.value = newLimit.value
        limit.category = newLimit.category

        await self.db.commit()
        await self.db.refresh(limit)
        return limit
    
    async def delete(self, id: int, userId: int):
        Limit = await self.db.get(ModelLimit, id)
        if not Limit:
            raise HTTPException(status_code=404, detail="Limite não encontrado")
        
        if Limit.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        await self.db.delete(Limit)
        await self.db.commit()
        return {"detail": "Limite deletado"}

    async def getById(self, id: int, userId: int):  
        limit = await self.db.get(ModelLimit, id)
        if not limit:
            raise HTTPException(status_code=404, detail="Limite não encontrado")

        if limit.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")

        return limit

    async def getAll(self, userId: int):
        metas = await self.db.query(ModelLimit).filter(ModelLimit.user_id == userId).all()
        return metas