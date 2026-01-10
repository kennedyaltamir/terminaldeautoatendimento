# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-09 00:05:00
import os
import redis
import logging
from typing import Optional

logger = logging.getLogger("TokenService")

class TokenService:
    """
    Gerencia a revogação de tokens JWT utilizando Redis.
    Foca em performance e segurança de sessões ativas.
    """
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis = None
        self.enabled = False
        self._initialize_connection()

    def _initialize_connection(self):
        try:
            # redis-py é "lazy", a conexão real só ocorre no primeiro comando.
            # Usamos ping() para validar o estado do serviço no boot.
            self.redis = redis.from_url(self.redis_url, decode_responses=True, socket_connect_timeout=2)
            self.redis.ping()
            self.enabled = True
            logger.info(f"🚀 Redis Blocklist conectado: {self.redis_url}")
        except Exception as e:
            logger.error(f"⚠️  Falha ao conectar no Redis para Blacklist: {e}")
            logger.warning("🛡️  SISTEMA EM MODO FAIL-OPEN: Revogação de tokens desabilitada por falta de infraestrutura.")
            self.enabled = False

    def revoke_token(self, jti: str, expires_in_seconds: int):
        """
        Adiciona o ID do token na blacklist com TTL igual ao tempo restante do token.
        """
        if not self.enabled or not jti:
            return
        
        try:
            # Chave: bl_ (blacklist) + jti
            self.redis.setex(f"bl_{jti}", expires_in_seconds, "revoked")
            logger.info(f"🚫 Token revogado e bloqueado no Redis: {jti}")
        except Exception as e:
            logger.error(f"Erro ao gravar na blacklist do Redis: {e}")

    def is_revoked(self, jti: Optional[str]) -> bool:
        """
        Verifica se o identificador do token consta na blacklist.
        """
        if not self.enabled or not jti:
            return False
        
        try:
            return self.redis.exists(f"bl_{jti}") > 0
        except Exception as e:
            logger.error(f"Erro ao consultar blacklist no Redis: {e}")
            return False

# Instância Global
token_service = TokenService()
