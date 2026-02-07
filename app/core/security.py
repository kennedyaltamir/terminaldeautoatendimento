"""
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 5.0.0 (Native Bcrypt Implementation)
 * DNA_ID: MF-CORE-SECURITY-V5-NATIVE
 * OBJETIVO: Engine de Segurança com Driver Nativo.
 * FIX: Remove dependência do Passlib para geração de hash devido a bugs com Bcrypt 4.0+.
 */
 """
import os
import hashlib
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import bcrypt  # Driver nativo (Obrigatório)

from jose import jwt, JWTError, ExpiredSignatureError
# Mantemos passlib apenas para compatibilidade de leitura (verify), não escrita
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

# --- CONFIGURAÇÃO ---
# Contexto apenas para verificar hashes antigos se existirem
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

security_logger = logging.getLogger("mesaflow.security")

def log_security_event(action: str, success: bool, metadata: dict):
    level = logging.INFO if success else logging.WARNING
    security_logger.log(level, f"SECURITY_AUDIT | {action} | SUCCESS={success} | {metadata}")

# --- PASSWORD OPERATIONS (NATIVE BCRYPT) ---

def get_password_hash(password: str) -> str:
    """
    Gera hash seguro usando DIRETAMENTE o driver Bcrypt.
    Isso contorna o bug do Passlib com senhas < 72 bytes.
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # 1. Truncamento Defensivo (Limite físico do Blowfish)
    # Codifica para bytes primeiro para garantir contagem correta
    pwd_bytes = password.encode('utf-8')
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
    
    # 2. Geração de Salt e Hash (Nativo)
    # Gera um hash compatível com o formato padrão ($2b$...)
    hash_bytes = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    
    # Retorna string para salvar no banco
    return hash_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Valida senha. Tenta método nativo primeiro, fallback para passlib.
    """
    if not hashed_password or not plain_password:
        return False
    
    # Preparação da entrada
    pwd_bytes = plain_password.encode('utf-8')
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
        
    # Conversão do hash do banco para bytes
    hash_bytes = hashed_password.encode('utf-8')

    try:
        # Tentativa 1: Driver Nativo (Rápido e Seguro)
        return bcrypt.checkpw(pwd_bytes, hash_bytes)
    except Exception:
        # Tentativa 2: Passlib (Legado/Compatibilidade)
        try:
            return pwd_context.verify(plain_password[:72], hashed_password)
        except Exception:
            return False

# --- TOKEN OPERATIONS ---
def create_token(data: dict, expires_delta: timedelta, token_type: str, scope: str = "user") -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    
    jti_payload = f"{data.get('sub')}{expire.timestamp()}{token_type}{os.urandom(8).hex()}"
    jti = hashlib.sha256(jti_payload.encode()).hexdigest()
    
    to_encode.update({
        "exp": expire,
        "iat": now,
        "type": token_type,
        "jti": jti,
        "scope": scope
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="TOKEN_EXPIRED")
    except JWTError as e:
        log_security_event("JWT_DECODE_FAIL", False, {"error": str(e)})
        raise HTTPException(status_code=401, detail="TOKEN_INVALID")

def extract_token_jti(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        return payload.get("jti", "")
    except JWTError:
        return ""

async def get_auth_payload(auth: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)) -> Dict[str, Any]:
    if not auth:
        raise HTTPException(status_code=401, detail="AUTHENTICATION_REQUIRED")
    return decode_token(auth.credentials)