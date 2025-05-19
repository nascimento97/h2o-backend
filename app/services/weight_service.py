from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.weight import Weight
from app.schemas.weight import WeightCreate

class WeightService:
    @staticmethod
    def create_weight(db: Session, data: WeightCreate) -> Weight:
        weight = Weight(value=data.value)
        db.add(weight)
        db.commit()
        db.refresh(weight)
        return weight
