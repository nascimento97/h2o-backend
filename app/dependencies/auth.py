from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime

from app.core.config import settings
from app.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Tabela para tokens revogados (opcional, implementar em DB)
# Exemplo de modelo: RevokedToken(token: str, revoked_at: datetime)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
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
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_exp: int = payload.get("exp")
        if datetime.utcfromtimestamp(token_exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except JWTError:
        raise credentials_exception

    # Checar blacklist (revoked tokens) antes de prosseguir
    # revoked = db.query(RevokedToken).filter_by(token=token).first()
    # if revoked:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    user = db.query(User).filter_by(name=username, is_deleted=False).first()
    if not user:
        raise credentials_exception
    return user

# função para invalidar token no logout (exemplo de uso)
def revoke_token(token: str, db: Session = Depends(get_db)):
    # Implementar lógica de revogação, ex: salvar token em tabela RevokedToken
    # revoked = RevokedToken(token=token, revoked_at=datetime.utcnow())
    # db.add(revoked)
    # db.commit()
    return True
