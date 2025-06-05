from fastapi import APIRouter, Depends, HTTPException
from api.data.db import get_db
from api.services.UserServices import UsuarioService
from api.schemas.User import User, UserLogin, UserResponse
from api.schemas.Transaction import TransactionResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.auth import get_user_id_from_token
from fastapi import Response

router = APIRouter()

@router.post("/add")
async def create(user: User, response: Response, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.create(user, response)

@router.get("/get/{id}", response_model=UserResponse)
async def get_By_Id(id: int, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.getById(id)

@router.delete("/delete")
async def delete(db: AsyncSession = Depends(get_db), id: int = Depends(get_user_id_from_token)):
    service = UsuarioService(db)
    return await service.deleteById(id)

@router.put("/editNome", response_model=UserResponse)
async def edit_nome(newName: str, password: str, db: AsyncSession = Depends(get_db), id: int = Depends(get_user_id_from_token)):
    service = UsuarioService(db)
    return await service.editNome(id, newName, password)

@router.put("/editSenha", response_model=UserResponse)
async def edit_senha(currentPassword: str, newPassword: str, db: AsyncSession = Depends(get_db), id: int = Depends(get_user_id_from_token)):
    service = UsuarioService(db)
    user = await service.editSenha(id, currentPassword, newPassword)
    return UserResponse.from_orm(user)

@router.post("/login")
async def Login(user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.login(user.email, user.password, response)

@router.get("/me", response_model=UserResponse)
async def get_By_Token(user_id: int = Depends(get_user_id_from_token), db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.getById(user_id)

@router.get("/historico", response_model=list[TransactionResponse])
async def get_historico(user_id: int = Depends(get_user_id_from_token), db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.getHistorico(user_id)