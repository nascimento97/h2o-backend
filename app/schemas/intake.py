# app/schemas/intake.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

ALLOWED_QUANTITIES: List[int] = [200, 350, 500]

class IntakeBase(BaseModel):
    quantity: int = Field(
        ..., example=200, description="Quantidade em ml"
    )

class IntakeCreate(IntakeBase):
    pass

class IntakeRead(IntakeBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class IntakeFilter(BaseModel):
    quantity: Optional[int] = Field(
        None, description="Filtrar por quantidade (200, 350, 500)"
    )
    date_from: Optional[datetime] = Field(
        None, description="Data inicial para filtro"
    )
    date_to: Optional[datetime] = Field(
        None, description="Data final para filtro"
    )
