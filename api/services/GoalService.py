from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from api.data.models.ModelGoal import ModelGoal
from api.data.models.ModelTransaction import ModelTransaction
from api.data.models.ModelCategory import ModelCategory
from api.schemas.Goal import GoalResponse

class GoalService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, goal: ModelGoal, userId: int):
        try:
            novo_goal = ModelGoal(
                name=goal.name,
                GoalValue=goal.GoalValue,
                CurrentValue=goal.CurrentValue,
                user_id=userId,
            )
            self.db.add(novo_goal)
            await self.db.commit()
            await self.db.refresh(novo_goal)

            stmt = (
                select(ModelGoal)
                .options(selectinload(ModelGoal.historico))
                .where(ModelGoal.id == novo_goal.id)
            )
            result = await self.db.execute(stmt)
            goal_completo = result.scalar_one()

            return GoalResponse.from_orm(goal_completo)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao criar meta: {str(e)}")

    async def editMeta(self, id: int, newName: str, newValue: float, userId: int):
        try:
            meta = await self.db.get(ModelGoal, id)
            if not meta:
                raise HTTPException(status_code=404, detail="Meta não encontrada")
            if meta.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado")

            meta.name = newName
            meta.GoalValue = newValue

            await self.db.commit()
            await self.db.refresh(meta)

            query = select(ModelTransaction).options(selectinload(ModelTransaction.category)).where(ModelTransaction.goal_id == id)
            result = await self.db.execute(query)
            historico = result.scalars().all()

            historico_serializado = []
            for tx in historico:
                historico_serializado.append({
                    "id": tx.id,
                    "type": tx.type,
                    "value": tx.value,
                    "date": tx.date,
                    "category": tx.category.name,
                    "goal_id": tx.goal_id,
                })

            return {
                "id": meta.id,
                "name": meta.name,
                "GoalValue": meta.GoalValue,
                "CurrentValue": meta.CurrentValue,
                "user_id": meta.user_id,
                "historico": historico_serializado,
            }
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao editar meta: {str(e)}")

    async def delete(self, id: int, userId: int):
        try:
            meta = await self.db.get(ModelGoal, id)
            if not meta:
                raise HTTPException(status_code=404, detail="Meta não encontrada")
            if meta.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado")

            query = select(ModelTransaction).where(ModelTransaction.goal_id == id).options(selectinload(ModelTransaction.category))
            result = await self.db.execute(query)
            transacoes = result.scalars().all()

            categorias_para_verificar = set()
            for tran in transacoes:
                if tran.category:
                    categorias_para_verificar.add(tran.category.id)

            for tran in transacoes:
                await self.db.delete(tran)

            for cat_id in categorias_para_verificar:
                query = select(ModelTransaction).where(
                    ModelTransaction.category_id == cat_id,
                    ModelTransaction.goal_id != id
                )
                result = await self.db.execute(query)
                restante = result.scalars().first()
                if not restante:
                    categoria = await self.db.get(ModelCategory, cat_id)
                    if categoria:
                        await self.db.delete(categoria)

            await self.db.delete(meta)
            await self.db.commit()
            return {"detail": "Meta deletada"}
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao deletar meta: {str(e)}")

    async def getById(self, id: int, userId: int):
        try:
            meta = await self.db.get(ModelGoal, id)
            if not meta:
                raise HTTPException(status_code=404, detail="Meta não encontrada")
            if meta.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado")

            query = select(ModelTransaction).where(
                ModelTransaction.goal_id == id
            ).options(
                selectinload(ModelTransaction.category)
            )
            result = await self.db.execute(query)
            historico = result.scalars().all()

            historico_serializado = []
            for tx in historico:
                historico_serializado.append({
                    "id": tx.id,
                    "type": tx.type,
                    "value": tx.value,
                    "date": tx.date,
                    "category": tx.category.name,
                    "goal_id": tx.goal_id,
                })

            return {
                "id": meta.id,
                "name": meta.name,
                "GoalValue": meta.GoalValue,
                "CurrentValue": meta.CurrentValue,
                "user_id": meta.user_id,
                "historico": historico_serializado,
            }
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar meta: {str(e)}")

    async def getHistorico(self, goal_id: int, userId: int):
        try:
            meta = await self.db.get(ModelGoal, goal_id)
            if not meta:
                raise HTTPException(status_code=404, detail="Meta não encontrada")
            if meta.user_id != userId:
                raise HTTPException(status_code=403, detail="Acesso negado")

            query = select(ModelTransaction).where(ModelTransaction.goal_id == goal_id)
            result = await self.db.execute(query)
            historico = result.scalars().all()

            return historico
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")

    async def getAll(self, userId: int):
        try:
            stmt = (
                select(ModelGoal)
                .options(
                    selectinload(ModelGoal.historico).selectinload(ModelTransaction.category)
                )
                .where(ModelGoal.user_id == userId)
            )
            result = await self.db.execute(stmt)
            metas = result.scalars().all()

            metas_serializadas = []
            for meta in metas:
                historico_serializado = []
                for tx in meta.historico:
                    historico_serializado.append({
                        "id": tx.id,
                        "type": tx.type,
                        "value": tx.value,
                        "date": tx.date,
                        "category": tx.category.name,
                        "goal_id": tx.goal_id,
                    })

                metas_serializadas.append({
                    "id": meta.id,
                    "name": meta.name,
                    "GoalValue": meta.GoalValue,
                    "CurrentValue": meta.CurrentValue,
                    "user_id": meta.user_id,
                    "historico": historico_serializado,
                })

            return metas_serializadas
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar metas: {str(e)}")
