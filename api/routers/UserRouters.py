from fastapi import APIRouter, Depends, HTTPException
from api.data.db import get_db
from api.services.UserServices import UsuarioService
from api.schemas.User import User, UserLogin, UserResponse
from api.schemas.Transaction import TransactionResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.auth import get_user_id_from_token

router = APIRouter()

@router.post("/add")
async def create(user: User, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.create(user)

@router.get("/get/{id}", response_model=UserResponse)
async def get_By_Id(id: int, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.getById(id)

@router.delete("/delete/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.deleteById(id)

@router.put("/editNome/{id}", response_model=UserResponse)
async def edit_nome(id: int, newName: str, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.editNome(id, newName)

@router.put("/editSenha/{id}", response_model=UserResponse)
async def edit_senha(id: int, password: str, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    user = await service.editSenha(id, password)
    return UserResponse.from_orm(user)

@router.post("/login")
async def Login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    usuario = await service.verificaSenha(user.email, user.password)
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = service._criar_token(usuario)
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
async def get_me(user_id: int = Depends(get_user_id_from_token)):
    return {"user_id": user_id}

@router.get("/historico", response_model=list[TransactionResponse])
async def get_historico(user_id: int = Depends(get_user_id_from_token), db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.getHistorico(user_id)