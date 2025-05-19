from datetime import datetime
from pydantic import BaseModel, Field

class WeightBase(BaseModel):
    value: float = Field(..., example=70.5)

class WeightCreate(WeightBase):
    pass

class WeightRead(WeightBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}