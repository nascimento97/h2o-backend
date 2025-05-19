# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import user_router, weight_router, intake_router

# Criar todas as tabelas no startup (ou usar Alembic em produção)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="h2o - Monitoramento de Consumo de Água",
    version="1.0.0",
    description="API para registrar e consultar ingestão de água por usuários",
)

# Configuração de CORS (ajuste origins conforme necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou lista de domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(user_router.router)
app.include_router(weight_router.router)
app.include_router(intake_router.router)

# Rota healthcheck
@app.get("/health", tags=["health"])
def health_check():
    """Verifica se a API está ativa"""
    return {"status": "ok"}
