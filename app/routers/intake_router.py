from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.schemas.intake import IntakeCreate, IntakeRead, IntakeFilter
from app.services.intake_service import IntakeService
from app.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/intake", tags=["intake"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=IntakeRead, status_code=status.HTTP_201_CREATED)
def add_intake(
    intake: IntakeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Registra ingestão de água para o usuário logado"""
    return IntakeService.add_intake(db, intake, current_user.id)

@router.get("/", response_model=List[IntakeRead])
def get_history(
    quantity: int = Query(None, description="Filtrar por quantidade (200, 350, 500)"),
    date_from: datetime = Query(None),
    date_to: datetime = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Recupera histórico de ingestão com filtros opcionais"""
    filters = IntakeFilter(quantity=quantity, date_from=date_from, date_to=date_to)
    return IntakeService.get_history(db, current_user.id, filters)
