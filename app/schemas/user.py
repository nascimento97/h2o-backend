from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal

class UserBase(BaseModel):
    name: str = Field(..., example="joao")

class UserCreate(UserBase):
    weight_id: int = Field(..., example=1)

class UserRead(UserBase):
    id: int
    weight_id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class UserLogin(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"