from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.data.models.ModelCategory import ModelCategory

class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, category: ModelCategory, userId: int):
        db_category = ModelCategory(
            goal_date=category.name,
            user_id=userId,
        )
        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)
        return db_category

    async def getAll(self, userId: int):
        category = await self.db.query(ModelCategory).filter(ModelCategory.user_id == userId).all()
        return category