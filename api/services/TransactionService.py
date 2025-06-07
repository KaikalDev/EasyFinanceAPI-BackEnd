from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.data.models.ModelTransaction import ModelTransaction
from api.data.models.ModelGoal import ModelGoal

class TransactionService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, tran: ModelTransaction, userId: int):
        db_tran = ModelTransaction(
            type=tran.type,
            value=tran.value,
            date=tran.date,
            category=tran.category,
            user_id=userId,
            goal_id=tran.goal_id
        )
        if tran.goal_id:
            goal = await self.db.get(ModelGoal, tran.goal_id)
            if not goal:
                raise HTTPException(status_code=404, detail="Meta não encontrada")
            if goal.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado à meta")

            goal.currentValue += tran.value
        self.db.add(db_tran)
        await self.db.commit()
        await self.db.refresh(db_tran)
        return db_tran

    async def edit(self, id: int, newTran: ModelTransaction, userId: int):
        tran = await self.db.get(ModelTransaction, id)
        if not tran:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        if tran.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        tran.type = newTran.type
        tran.value = newTran.value
        tran.date = newTran.date
        tran.category = newTran.category
        tran.goal_id = newTran.goal_id

        await self.db.commit()
        await self.db.refresh(tran)
        return tran
    
    async def delete(self, id: int, userId: int):
        tran = await self.db.get(ModelTransaction, id)
        if not tran:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        if tran.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        await self.db.delete(tran)
        await self.db.commit()
        return {"detail": "Transaction deleted"}

    async def getById(self, id: int, userId: int):  
        tran = await self.db.get(ModelTransaction, id)
        if not tran:
            raise HTTPException(status_code=404, detail="Transação não encontrada")

        if tran.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")

        return tran
