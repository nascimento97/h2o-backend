# tests/conftest.py
import sys
import pathlib

# Adiciona o diretório raiz do projeto ao sys.path para importar o pacote 'app'
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.core.config import settings

# Configurações do banco de teste (in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria todas as tabelas antes dos testes
Base.metadata.create_all(bind=engine)

# Override da dependência get_db para usar o DB de teste
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    """TestClient configurado com o app e DB in-memory"""
    with TestClient(app) as c:
        yield c
