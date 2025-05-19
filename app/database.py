from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# URL de conexão para SQLite (banco local h2o.db no diretório raiz do projeto)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{settings.PROJECT_NAME}.db"

# Para SQLite precisamos desse argumento para permitir conexões em múltiplas threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal é a fábrica de sessões do SQLAlchemy
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base é a classe para todos os modelos (models) herdarem
Base = declarative_base()


def get_db():
    """
    Dependência do FastAPI para obter uma sessão de DB.
    Garante que a sessão seja fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
