from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Weight(BaseModel):
    __tablename__ = "weights"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)

    users = relationship("User", back_populates="weight")
