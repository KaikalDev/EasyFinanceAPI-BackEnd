from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from api.data.models.ModelCategory import ModelCategory
from api.data.models.ModelTransaction import ModelTransaction
from api.data.models.ModelGoal import ModelGoal
from api.schemas.Transaction import Transaction

class TransactionService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, tran: Transaction, userId: int):
        try:
            def format_category_name(name: str):
                return name.strip().lower().capitalize()

            category_name_cap = format_category_name(tran.category)

            if tran.goal_id:
                goal = await self.db.get(ModelGoal, tran.goal_id)
                if not goal:
                    raise HTTPException(status_code=404, detail="Meta não encontrada")
                if goal.user_id != userId:
                    raise HTTPException(status_code=403, detail="Acesso negado à meta")

                new_current = goal.CurrentValue + tran.value if tran.type == 'gasto' else goal.CurrentValue - tran.value
                if new_current < 0:
                    raise HTTPException(status_code=400, detail="Operação resultaria em saldo negativo da meta")

                goal.CurrentValue = new_current
                self.db.add(goal)
                await self.db.flush()

                category_name_cap = f"Meta: {goal.name.capitalize()}"

            result = await self.db.execute(
                select(ModelCategory).where(ModelCategory.name == category_name_cap)
            )
            category_obj = result.scalars().first()

            if not category_obj:
                category_obj = ModelCategory(name=category_name_cap, user_id=userId)
                self.db.add(category_obj)
                await self.db.flush()

            db_tran = ModelTransaction(
                type=tran.type,
                value=tran.value,
                date=tran.date,
                category_id=category_obj.id,
                user_id=userId,
                goal_id=tran.goal_id
            )

            self.db.add(db_tran)
            await self.db.flush()
            await self.db.commit()
            await self.db.refresh(db_tran)

            return {
                "id": db_tran.id,
                "type": db_tran.type,
                "value": db_tran.value,
                "date": db_tran.date.isoformat() if db_tran.date else None,
                "category": category_name_cap,
                "goal_id": db_tran.goal_id,
                "user_id": db_tran.user_id
            }
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

    async def edit(self, id: int, newTran: ModelTransaction, userId: int):
        try:
            tran = await self.db.get(ModelTransaction, id)
            if not tran:
                raise HTTPException(status_code=404, detail="Transaction not found")
            
            if tran.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado")

            if tran.goal_id:
                old_goal = await self.db.get(ModelGoal, tran.goal_id)
                if old_goal and old_goal.user_id == userId:
                    if tran.type == 'gasto':
                        old_goal.CurrentValue -= tran.value
                    else:
                        old_goal.CurrentValue += tran.value
                    self.db.add(old_goal)

            category_name_cap = newTran.category.lower().capitalize()

            if newTran.goal_id:
                goal = await self.db.get(ModelGoal, newTran.goal_id)
                if not goal or goal.user_id != userId:
                    raise HTTPException(status_code=403, detail="Acesso negado à nova meta")

                new_current = goal.CurrentValue + newTran.value if newTran.type == 'gasto' else goal.CurrentValue - newTran.value
                if new_current < 0:
                    raise HTTPException(status_code=400, detail="Operação resultaria em saldo negativo da meta")

                goal.CurrentValue = new_current
                self.db.add(goal)
                category_name_cap = f"Meta: {goal.name.capitalize()}"

            category = await self.db.execute(
                select(ModelCategory).where(ModelCategory.name == category_name_cap)
            )
            category_obj = category.scalars().first()
            if not category_obj:
                category_obj = ModelCategory(name=category_name_cap, user_id=userId)
                self.db.add(category_obj)
                await self.db.flush()

            tran.type = newTran.type
            tran.value = newTran.value
            tran.date = newTran.date
            tran.category_id = category_obj.id
            tran.goal_id = newTran.goal_id

            await self.db.commit()
            await self.db.refresh(tran)

            return {
                "id": tran.id,
                "type": tran.type,
                "value": tran.value,
                "date": tran.date.isoformat() if tran.date else None,
                "category": category_name_cap,
                "goal_id": tran.goal_id,
                "user_id": tran.user_id
            }
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

    async def delete(self, id: int, userId: int):
        try:
            tran = await self.db.get(ModelTransaction, id)
            if not tran:
                raise HTTPException(status_code=404, detail="Transaction not found")
            
            if tran.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado")

            if tran.goal_id:
                goal = await self.db.get(ModelGoal, tran.goal_id)
                if goal and goal.user_id == userId:
                    goal.CurrentValue -= tran.value
                    self.db.add(goal)

            await self.db.delete(tran)
            await self.db.commit()
            return {"detail": "Transaction deleted"}
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

    async def getById(self, id: int, userId: int):  
        try:
            tran = await self.db.get(ModelTransaction, id)
            if not tran:
                raise HTTPException(status_code=404, detail="Transação não encontrada")

            if tran.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado")

            return tran
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")
