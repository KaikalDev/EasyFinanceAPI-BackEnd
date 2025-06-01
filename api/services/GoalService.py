from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.data.models import ModelGoal

class GoalService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, goal: ModelGoal, userId: int):
        db_tran = ModelGoal(
            goal_date=goal.goal_date,
            goal_value=goal.goal_value,
            name=goal.name,
            user_id=userId,
        )
        self.db.add(db_tran)
        await self.db.commit()
        await self.db.refresh(db_tran)
        return db_tran

    async def edit(self, id: int, newGoal: ModelGoal, userId: int):
        goal = await self.db.get(ModelGoal, id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        if goal.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        goal.name = newGoal.name
        goal.goal_date = newGoal.goal_date
        goal.goal_value = newGoal.goal_value

        await self.db.commit()
        await self.db.refresh(goal)
        return goal
    
    async def delete(self, id: int, userId: int):
        goal = await self.db.get(ModelGoal, id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        if goal.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        await self.db.delete(goal)
        await self.db.commit()
        return {"detail": "Goal deleted"}

    async def getById(self, id: int, userId: int):  
        Goal = await self.db.get(ModelGoal, id)
        if not Goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        if Goal.user_id != userId:
            raise HTTPException(status_code=403, detail="Acesso negado")

        return Goal
