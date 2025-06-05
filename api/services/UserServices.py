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
from jose import jwt
from datetime import datetime, timedelta
from api.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _criar_token(self, user: ModelUser):
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    async def create(self, user: User, response: Response):
        hashed = pwd_context.hash(user.password)
        data = user.dict()
        data["password"] = hashed

        userToAdd = ModelUser(**data)
        self.db.add(userToAdd)
        await self.db.flush()

        await self.db.refresh(userToAdd)

        categorias = [
            "Alimantação", "Aluguel", "Saúde", "Lazer",
            "Cofrinho", "Agua", "Luz", "Internet"
        ]
        categorias_obj = [
            ModelCategory(user_id=userToAdd.id, name=cat) for cat in categorias
        ]
        self.db.add_all(categorias_obj)

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

    async def login(self, email: str, password: str, response: Response):
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

        return {"msg": "Login efetuado com sucesso"}

    async def editNome(self, id: int, newName: str):
        user = await self.db.get(ModelUser, id)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        user.name = newName
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def editSenha(self, id: int, newPassword: str):
        user = await self.db.get(ModelUser, id)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        hashed_password = pwd_context.hash(newPassword)
        user.password = hashed_password
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def getById(self, id: int):
        result = await self.db.execute(select(ModelUser).where(ModelUser.id == id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return user

    async def verificaSenha(self, email: str, password: str):
        result = await self.db.execute(select(ModelUser).where(ModelUser.email == email))
        usuario = result.scalar_one_or_none()
        if usuario and pwd_context.verify(password, usuario.password):
            return usuario
        return None

    async def deleteById(self, id: int):
        await self.db.execute(delete(ModelCategory).where(ModelCategory.user_id == id))
        await self.db.execute(delete(ModelLimit).where(ModelLimit.user_id == id))
        await self.db.execute(delete(ModelTransaction).where(ModelTransaction.user_id == id))
        await self.db.execute(delete(ModelGoal).where(ModelGoal.user_id == id))
        query = delete(ModelUser).where(ModelUser.id == id)
        result = await self.db.execute(query)
        await self.db.commit()
        if result.rowcount == 0:
            raise Exception("user not found")
        return {"detail": "User deleted"}
    
    async def getHistorico(self, userId: int):
        query = select(ModelUser).options(selectinload(ModelUser.historico)).where(ModelUser.id == userId)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return user.historical
