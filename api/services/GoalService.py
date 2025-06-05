from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.data.models.ModelGoal import ModelGoal
from api.data.models.ModelTransaction import ModelTransaction
from sqlalchemy.future import select
from sqlalchemy import delete

class GoalService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, goal: ModelGoal, userId: int):
        PiggyDb = ModelGoal(
            name=goal.name,
            GoalValue=goal.GoalValue,
            CurrentValue=goal.CurrentValue,
            user_id=userId,
        )
        self.db.add(PiggyDb)
        await self.db.commit()
        await self.db.refresh(PiggyDb)
        return PiggyDb

    async def editName(self, id: int, newName: str, userId: int):
        meta = await self.db.get(ModelGoal, id)
        if not meta:
            raise HTTPException(status_code=404, detail="piggy not found")
        
        if meta.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        meta.name = newName

        await self.db.commit()
        await self.db.refresh(meta)
        return meta
    
    async def delete(self, id: int, userId: int):
        await self.db.execute(delete(ModelTransaction).where(ModelTransaction.user_id == id))
        meta = await self.db.get(ModelGoal, id)
        if not meta:
            raise HTTPException(status_code=404, detail="Meta não encontrada")
        
        if meta.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        await self.db.delete(meta)
        await self.db.commit()
        return {"detail": "meta deletada"}

    async def getById(self, id: int, userId: int):  
        meta = await self.db.get(ModelGoal, id)
        if not meta:
            raise HTTPException(status_code=404, detail="Meta não encontrada")

        if meta.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")

        return meta
    
    async def getHistorico(self, goal_id: int, userId: int):
        meta = await self.db.get(ModelGoal, goal_id)
        if not meta:
            raise HTTPException(status_code=404, detail="Meta não encontrada")

        if meta.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")

        query = select(ModelTransaction).where(ModelTransaction.goal_id == goal_id)
        result = await self.db.execute(query)
        historico = result.scalars().all()

        return historico

    async def getAll(self, userId: int):
        metas = await self.db.query(ModelGoal).filter(ModelGoal.user_id == userId).all()
        return metas
