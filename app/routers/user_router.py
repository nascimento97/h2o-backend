from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead, UserLogin, Token
from app.services.user_service import UserService
from app.database import get_db
from app.dependencies.auth import get_current_user, revoke_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário com peso inicial"""
    return UserService.create_user(db, user)

@router.post("/login", response_model=Token)
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Faz login e retorna token JWT de acesso"""
    token = UserService.login_user(db, credentials)
    return {"access_token": token}

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(
    token: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Revoga o token de acesso"""
    revoke_token(token, db)
    return {"detail": "Logout successful"}
