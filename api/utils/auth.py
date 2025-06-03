from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from api.utils.config import SECRET_KEY, ALGORITHM
from fastapi import Cookie

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_user_id_from_token(access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Não autenticado")
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
