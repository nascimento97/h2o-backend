from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import and_
from datetime import datetime
from app.models.intake import Intake
from app.schemas.intake import IntakeCreate, IntakeFilter, ALLOWED_QUANTITIES

class IntakeService:
    @staticmethod
    def add_intake(db: Session, data: IntakeCreate, user_id: int) -> Intake:
        if data.quantity not in ALLOWED_QUANTITIES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid quantity")
        intake = Intake(quantity=data.quantity, user_id=user_id)
        db.add(intake)
        db.commit()
        db.refresh(intake)
        return intake

    @staticmethod
    def get_history(db: Session, user_id: int, filters: IntakeFilter) -> List[Intake]:
        query = db.query(Intake).filter(Intake.user_id == user_id, Intake.is_deleted == False)
        if filters.quantity is not None:
            query = query.filter(Intake.quantity == filters.quantity)
        if filters.date_from is not None:
            query = query.filter(Intake.created_at >= filters.date_from)
        if filters.date_to is not None:
            query = query.filter(Intake.created_at <= filters.date_to)
        return query.order_by(Intake.created_at.desc()).all()
