import uuid
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete
from fastapi import Response
from api.data.models.ModelUser import ModelUser
from api.data.models.ModelTransaction import ModelTransaction
from api.data.models.ModelCategory import ModelCategory
from api.data.models.ModelGoal import ModelGoal
from api.data.models.ModelLimit import ModelLimit
from api.schemas.User import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from api.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _criar_token(self, user: ModelUser):
        try:
            payload = {
                "sub": str(user.id),
                "email": user.email,
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                "jti": str(uuid.uuid4())
            }
            return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erro ao gerar token")

    async def create(self, user: User, response: Response):
        try:
            hashed = pwd_context.hash(user.password)
            data = user.dict()
            data["password"] = hashed

            userToAdd = ModelUser(**data)
            self.db.add(userToAdd)
            await self.db.flush()
            await self.db.refresh(userToAdd)

            await self.db.commit()
            await self.db.refresh(userToAdd)

            token = self._criar_token(userToAdd)
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                max_age=60 * 60 * 24 * 7,
                samesite="None",
                secure=True
            )

            return {"msg": "Usuário criado com sucesso"}
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Erro ao criar usuário")

    async def login(self, email: str, password: str, response: Response):
        try:
            result = await self.db.execute(select(ModelUser).where(ModelUser.email == email))
            user = result.scalar_one_or_none()
            if not user or not pwd_context.verify(password, user.password):
                raise HTTPException(status_code=401, detail="Email ou senha inválidos")

            token = self._criar_token(user)
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                max_age=60 * 60 * 24 * 7,
                samesite="None",
                secure=True
            )

            return {"msg": token}
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=500, detail="Erro ao realizar login")

    async def editNome(self, id: int, newName: str, password: str):
        try:
            user = await self.db.get(ModelUser, id)
            if not user:
                raise HTTPException(status_code=404, detail="user not found")
            if not pwd_context.verify(password, user.password):
                raise HTTPException(status_code=400, detail="senha atual incorreta")

            user.name = newName
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except HTTPException:
            raise
        except Exception:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Erro ao editar nome")

    async def editSenha(self, id: int, currentPassword: str, newPassword: str):
        try:
            user = await self.db.get(ModelUser, id)
            if not user:
                raise HTTPException(status_code=404, detail="user not found")
            if not pwd_context.verify(currentPassword, user.password):
                raise HTTPException(status_code=400, detail="senha atual incorreta")

            hashed_password = pwd_context.hash(newPassword)
            user.password = hashed_password
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except HTTPException:
            raise
        except Exception:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Erro ao alterar senha")

    async def getById(self, id: int):
        try:
            result = await self.db.execute(select(ModelUser).where(ModelUser.id == id))
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            return user
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=500, detail="Erro ao buscar usuário")

    async def verificaSenha(self, email: str, password: str):
        try:
            result = await self.db.execute(select(ModelUser).where(ModelUser.email == email))
            usuario = result.scalar_one_or_none()
            if usuario and pwd_context.verify(password, usuario.password):
                return usuario
            return None
        except Exception:
            return None

    async def deleteById(self, id: int):
        try:
            await self.db.execute(delete(ModelCategory).where(ModelCategory.user_id == id))
            await self.db.execute(delete(ModelLimit).where(ModelLimit.user_id == id))
            await self.db.execute(delete(ModelTransaction).where(ModelTransaction.user_id == id))
            await self.db.execute(delete(ModelGoal).where(ModelGoal.user_id == id))
            query = delete(ModelUser).where(ModelUser.id == id)
            result = await self.db.execute(query)
            await self.db.commit()
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            return {"detail": "User deleted"}
        except HTTPException:
            raise
        except Exception:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Erro ao deletar usuário")

    async def getHistorico(self, user_id: int):
        try:
            query = (
                select(ModelTransaction)
                .where(ModelTransaction.user_id == user_id)
                .options(selectinload(ModelTransaction.category))
            )
            result = await self.db.execute(query)
            transactions = result.scalars().all()

            response = []
            for tran in transactions:
                response.append({
                    "id": tran.id,
                    "type": tran.type,
                    "value": tran.value,
                    "date": tran.date.isoformat() if hasattr(tran.date, 'isoformat') else tran.date,
                    "category": tran.category.name if tran.category else None,
                    "goal_id": tran.goal_id,
                })

            return response
        except Exception:
            raise HTTPException(status_code=500, detail="Erro ao buscar histórico de transações")

    async def logout(self, response: Response):
        try:
            response.delete_cookie(
                key="access_token",
                httponly=True,
                samesite="None",
                secure=True
            )
            return {"msg": "Logout efetuado com sucesso"}
        except Exception:
            raise HTTPException(status_code=500, detail="Erro ao efetuar logout")
