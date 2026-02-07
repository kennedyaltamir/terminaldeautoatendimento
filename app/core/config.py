# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-05 01:35:00
"""
//
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 10.1.0 (Consolidated Master)
 * OBJETIVO: Mapeamento e validação integral das variáveis de ambiente (.env) via Pydantic Settings.
 * Comportamento esperado: O Kernel carrega este arquivo no boot. Ele valida a existência de chaves críticas. 
 * Caso alguma variável obrigatória falte ou o formato seja inválido, o sistema aborta o boot.
 */
//
"""

import os
import json
from typing import List, Union, Optional, Any
from pydantic import field_validator, EmailStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- 1. CORE INFRA ---
    PROJECT_NAME: str = "MesaFlow OS"
    VERSION: str = "10.2.0"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # --- 2. DATABASE & CACHE ---
    DATABASE_URL: str
    REDIS_URL: str
    REDIS_DISABLED: bool = False

    # --- 3. SECURITY ---
    SECRET_KEY: str
    SUPER_ADMIN_SECRET: str
    GOOGLE_CLIENT_ID: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 

    # --- 4. FINTECH: STRIPE ---
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PRO_PRICE_ID: Optional[str] = None

    # --- 5. FINTECH: MERCADO PAGO ---
    MP_ACCESS_TOKEN: Optional[str] = None
    MP_APP_ID: Optional[str] = None
    MP_CLIENT_SECRET: Optional[str] = None
    MP_REDIRECT_URI: Optional[str] = None

    # --- 6. INTEGRATORS: IFOOD ---
    IFOOD_CLIENT_ID: Optional[str] = None
    IFOOD_CLIENT_SECRET: Optional[str] = None
    IFOOD_WEBHOOK_SECRET: Optional[str] = None

    # --- 7. COMMUNICATION ---
    WHATSAPP_API_URL: Optional[str] = None
    WHATSAPP_API_TOKEN: Optional[str] = None
    WHATSAPP_INSTANCE: Optional[str] = None

    # --- 8. FISCAL ---
    FISCAL_PROVIDER: str = "mock"
    FISCAL_ENV: str = "sandbox"
    FISCAL_TOKEN: Optional[str] = None
    FISCAL_PRODUCTION_CONFIRMED: bool = False

    # --- 9. INFRA: EMAIL (SMTP) ---
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None

    # --- 10. INFRA: STORAGE (AWS S3 / R2) ---
    AWS_BUCKET_NAME: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_ENDPOINT_URL: Optional[str] = None

    # --- 11. OBSERVABILITY ---
    SENTRY_DSN_BACKEND: Optional[str] = None

    # --- 12. CORS SETTINGS ---
    # Mudamos o tipo para Any temporariamente no validador 'before' para evitar o crash do json.loads
    BACKEND_CORS_ORIGINS: Any = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "http://localhost:3001"
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """
        🛡️ HARDENING: Converte string CSV do .env em lista real.
        Ignora a tentativa automática do Pydantic de ler como JSON.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        # Se for um JSON válido (string que começa com [), tenta carregar
        if isinstance(v, str) and v.startswith("["):
            try:
                return json.loads(v)
            except:
                return [v]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

# --- BOOT VALIDATION ---
try:
    settings = Settings()
except ValidationError as e:
    print("\n" + "!"*60)
    print("🚨 FALHA CRÍTICA DE CONFIGURAÇÃO (.env)")
    print("!"*60)
    print(e)
    import sys
    sys.exit(1)