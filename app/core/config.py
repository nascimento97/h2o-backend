# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Configurações centrais da aplicação, lidas do .env automaticamente.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # Nome do projeto
    PROJECT_NAME: str = "h2o"
    # Chave secreta para assinar os tokens JWT
    SECRET_KEY: str = "supersecretkey"  # sempre sobrescreva via .env em produção!
    # Algoritmo de assinatura
    ALGORITHM: str = "HS256"
    # Duração do token de acesso (em horas)
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24

# Instância global de configurações
settings = Settings()
