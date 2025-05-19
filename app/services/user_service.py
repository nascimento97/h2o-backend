from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import user as user_model, weight as weight_model
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.core.security import create_access_token
from datetime import timedelta

class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> user_model.User:
        # Verifica se nome já existe
        existing = db.query(user_model.User).filter_by(name=user_data.name, is_deleted=False).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        # Cria peso inicial
        weight = weight_model.Weight(value=user_data.weight_id)
        db.add(weight)
        db.commit()
        db.refresh(weight)
        # Cria usuário referenciando peso
        user = user_model.User(name=user_data.name, weight_id=weight.id)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login_user(db: Session, credentials: UserLogin) -> str:
        # Busca usuário por nome
        user = db.query(user_model.User).filter_by(name=credentials.name, is_deleted=False).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        # Gera token JWT
        token = create_access_token(subject=user.name)
        return token
