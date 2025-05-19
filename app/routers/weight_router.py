from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.weight import WeightCreate, WeightRead
from app.services.weight_service import WeightService
from app.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/weights", tags=["weights"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=WeightRead, status_code=status.HTTP_201_CREATED)
def create_weight(
    weight: WeightCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo registro de peso"""
    return WeightService.create_weight(db, weight)
