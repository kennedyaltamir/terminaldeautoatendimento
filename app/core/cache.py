# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-10 16:20:00
import os
import json
import logging
import redis
import inspect
from typing import Optional, Any, Callable
from functools import wraps
from fastapi import Request
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger("CacheService")

class CacheService:
    _client: Optional[redis.Redis] = None
    _enabled = False

    @classmethod
    def initialize(cls):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            cls._client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=2
            )
            cls._client.ping()
            cls._enabled = True
            logger.info(f"🚀 Redis Cache conectado: {redis_url}")
        except Exception as e:
            logger.warning(f"⚠️ Redis Cache indisponível: {e}. Modo bypass ativado.")
            cls._enabled = False

    @classmethod
    def get(cls, key: str) -> Optional[str]:
        if not cls._enabled or not cls._client:
            return None
        try:
            return cls._client.get(key)
        except Exception as e:
            logger.error(f"Erro ao ler cache (key={key}): {e}")
            return None

    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300):
        if not cls._enabled or not cls._client:
            return
        try:
            # CORREÇÃO CRÍTICA: Usa jsonable_encoder para converter objetos SQLAlchemy/Pydantic
            # em tipos primitivos JSON antes de serializar para string.
            serializable_data = jsonable_encoder(value)
            serialized_value = json.dumps(serializable_data)
            cls._client.setex(key, ttl, serialized_value)
        except Exception as e:
            logger.error(f"Erro ao gravar cache (key={key}): {e}")

    @classmethod
    def delete(cls, pattern: str):
        if not cls._enabled or not cls._client:
            return
        try:
            keys = cls._client.keys(pattern)
            if keys:
                cls._client.delete(*keys)
                logger.info(f"🧹 Cache limpo: {pattern}")
        except Exception as e:
            logger.error(f"Erro ao limpar cache (pattern={pattern}): {e}")

    @classmethod
    def invalidate_menu(cls, slug: str):
        cls.delete(f"menu:{slug}*")

# Inicializa o serviço
CacheService.initialize()

def cache_response(ttl: int = 60, key_prefix: str = ""):
    """
    Decorator de cache inteligente que suporta funções síncronas e assíncronas.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request") or next((arg for arg in args if isinstance(arg, Request)), None)
            
            if not request:
                # Se não houver request, executa a função normalmente
                res = func(*args, **kwargs)
                return await res if inspect.isawaitable(res) else res

            try:
                final_prefix = key_prefix.format(**kwargs) if key_prefix else ""
            except:
                final_prefix = key_prefix
                
            cache_key = f"{final_prefix}:{request.url.path}:{request.url.query}"

            # 1. Tentar obter do cache
            cached_data_str = CacheService.get(cache_key)
            if cached_data_str:
                try:
                    return json.loads(cached_data_str)
                except:
                    pass

            # 2. Executar a função (detectando se é async ou sync)
            res = func(*args, **kwargs)
            response_data = await res if inspect.isawaitable(res) else res
            
            # 3. Salvar no cache
            try:
                CacheService.set(cache_key, response_data, ttl)
            except Exception as e:
                logger.warning(f"Falha ao cachear: {e}")
                
            return response_data
        return wrapper
    return decorator
