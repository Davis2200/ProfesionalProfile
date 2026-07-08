from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    # Metadatos del Proyecto
    PROJECT_NAME: str = "The Tranquil Journey API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Configuración de Entorno
    ENVIRONMENT: str = "development"  # development, production
    DEBUG: bool = False
    
    # Seguridad y CORS
    # En producción, esto debe ser una lista explícita (ej. tu dominio de Next.js)
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Supabase (Base de Datos y Auth)
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # Integraciones de Acto III y IV
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    RESEND_API_KEY: str
    
    # OAuth (GitHub/LinkedIn via Supabase)
    OAUTH_CLIENT_ID_GITHUB: str = ""
    OAUTH_CLIENT_ID_LINKEDIN: str = ""

    # Control de OpenAPI (TRD §5)
    @property
    def openapi_url(self) -> str:
        # Solo mostrar docs en desarrollo para evitar "Security through obscurity" innecesario
        # pero protegiendo la superficie de ataque en producción [5, 6]
        return f"{self.API_V1_STR}/openapi.json" if self.ENVIRONMENT == "development" else ""

    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=True
    )

settings = Settings()