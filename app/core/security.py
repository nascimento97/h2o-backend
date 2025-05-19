from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings

# Rota de obtenção de token (login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(subject: str) -> str:
    """
    Gera um JWT com 'sub' = subject e expiração configurada em horas.
    """
    expire = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Decodifica e valida um JWT. Retorna o 'sub' (nome do usuário) se válido.
    Lança HTTPException 401 em caso de falha.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Aqui você pode checar a blacklist de tokens revogados (implementar conforme necessário)
    # if is_token_revoked(token):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    return username
