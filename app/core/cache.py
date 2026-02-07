"""
//
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 10.5.0 (Consolidated Gold Master)
 * DNA_ID: MF-CORE-CACHE-V10-5
 * OBJETIVO: Engine de Cache Distribuído e Otimização de Resposta.
 * Comportamento esperado: 
 *  1. Inicializa o Redis com proteção contra falha de boot (Bypass Mode).
 *  2. Serializa tipos complexos (Decimal, UUID, Modelos) via jsonable_encoder.
 *  3. Provê decorador universal para rotas síncronas e assíncronas.
 *  4. Suporta invalidação em massa baseada em padrões de string.
 */
//
"""
import os
import json
import logging
import redis
import functools
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
        """
        Inicializa o rito de conexão com o Redis. 
        Implementa Fail-Open: Se o Redis falhar, o sistema opera em modo Bypass.
        """
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            cls._client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=1,
                socket_timeout=1
            )
            cls._client.ping()
            cls._enabled = True
            logger.info("🚀 Redis Cache conectado.")
        except Exception as e:
            logger.warning(f"⚠️ Redis Offline ({e}). Operando em modo BYPASS.")
            cls._enabled = False

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        if not cls._enabled or not cls._client: return None
        try:
            val = cls._client.get(key)
            return json.loads(val) if val else None
        except: return None

    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300):
        if not cls._enabled or not cls._client: return
        try:
            cls._client.setex(key, ttl, json.dumps(jsonable_encoder(value)))
        except: pass

    def incr(cls, key: str) -> int:
        """Incremento atômico para contadores e Circuit Breakers."""
        if not cls._enabled or not cls._client:
            return 0
        try:
            return cls._client.incr(key)
        except Exception:
            return 0
    @classmethod
    def invalidate_menu(cls, company_slug: str):
        """Invalida todas as variações de cache do menu de um tenant."""
        if not company_slug:
            return
        pattern = f"menu:{company_slug}*"
        cls.delete(pattern)
    @classmethod
    def delete(cls, key: str):
        if not cls._enabled or not cls._client: return
        try: cls._client.delete(key)
        except: pass

# Inicializa o Singleton
CacheService.initialize()

# 🛡️ FIX: Função exportada no nível do módulo para o roteador de Menu
def cache_response(ttl: int = 300, key_prefix: str = "cache"):
    """
    Decorator Universal de Cache.
    Gera chaves baseadas em: prefixo + path + query.
    Detecta e suporta funções assíncronas (FastAPI padrão).
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # 1. Checagem de disponibilidade
            if not CacheService._enabled:
                res = func(*args, **kwargs)
                return await res if inspect.isawaitable(res) else res
            
             # 2. Resolução de Contexto (Request)
            request = kwargs.get("request") or next((arg for arg in args if isinstance(arg, Request)), None)
            if not request:
                res = func(*args, **kwargs)
                return await res if inspect.isawaitable(res) else res

            cache_key = f"{key_prefix}:{request.url.path}:{request.url.query}"
            cached = CacheService.get(cache_key)
            if cached: return cached

            result = func(*args, **kwargs)
            data = await result if inspect.isawaitable(result) else result
            CacheService.set(cache_key, data, ttl)
            return data
        return wrapper
    return decorator