from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime
from app.database import Base

class SoftDeleteMixin:
    """
    Mixin para adicionar soft delete em todos os modelos.
    Todos os registros terão `is_deleted` e `deleted_at`.
    """
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

class TimestampMixin:
    """
    Mixin para adicionar timestamps de criação e atualização.
    """
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class BaseModel(Base, SoftDeleteMixin, TimestampMixin):
    __abstract__ = True
