from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    weight_id = Column(Integer, ForeignKey("weights.id"), nullable=False)

    weight = relationship("Weight", back_populates="users")
    intakes = relationship("Intake", back_populates="user")
