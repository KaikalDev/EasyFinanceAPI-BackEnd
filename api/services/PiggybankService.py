from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.data.models import ModelPiggybank, ModelTransaction
from sqlalchemy.future import select
from sqlalchemy import delete

class PiggyBankService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, piggybank: ModelPiggybank, userId: int):
        PiggyDb = ModelPiggybank(
            name=piggybank.name,
            user_id=userId,
        )
        self.db.add(PiggyDb)
        await self.db.commit()
        await self.db.refresh(PiggyDb)
        return PiggyDb

    async def editName(self, id: int, newName: str, userId: int):
        piggy = await self.db.get(ModelPiggybank, id)
        if not piggy:
            raise HTTPException(status_code=404, detail="piggy not found")
        
        if piggy.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        piggy.name = newName

        await self.db.commit()
        await self.db.refresh(piggy)
        return piggy
    
    async def delete(self, id: int, userId: int):
        await self.db.execute(delete(ModelTransaction).where(ModelTransaction.user_id == id))
        piggy = await self.db.get(ModelPiggybank, id)
        if not piggy:
            raise HTTPException(status_code=404, detail="Piggy not found")
        
        if piggy.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        await self.db.delete(piggy)
        await self.db.commit()
        return {"detail": "Piggy deleted"}

    async def getById(self, id: int, userId: int):  
        piggy = await self.db.get(ModelPiggybank, id)
        if not piggy:
            raise HTTPException(status_code=404, detail="Piggy not found")

        if piggy.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")

        return piggy
    
    async def getHistorico(self, piggybank_id: int, userId: int):
        piggy = await self.db.get(ModelPiggybank, piggybank_id)
        if not piggy:
            raise HTTPException(status_code=404, detail="Piggybank não encontrado")

        if piggy.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")

        query = select(ModelTransaction).where(ModelTransaction.cofrinho_id == piggybank_id)
        result = await self.db.execute(query)
        historico = result.scalars().all()

        return historico
