import os
import json
import logging
import redis
from typing import Optional, Any, Callable
from functools import wraps
from fastapi import Request, Response

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
        except Exception:
            return None

    @classmethod
    def set(cls, key: str, value: str, ttl: int = 300):
        if not cls._enabled or not cls._client:
            return
        try:
            cls._client.setex(key, ttl, value)
        except Exception as e:
            logger.error(f"Erro ao gravar cache: {e}")

    @classmethod
    def delete(cls, pattern: str):
        """Deleta chaves baseadas em um padrão (ex: menu:*)"""
        if not cls._enabled or not cls._client:
            return
        try:
            keys = cls._client.keys(pattern)
            if keys:
                cls._client.delete(*keys)
                logger.info(f"🧹 Cache limpo: {pattern} ({len(keys)} chaves)")
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {e}")

    @classmethod
    def invalidate_menu(cls, slug: str):
        """Atalho para invalidar o menu de uma empresa específica"""
        cls.delete(f"menu:{slug}")

# Inicializa na importação (Singleton simples)
CacheService.initialize()

def cache_response(ttl: int = 60, key_prefix: str = ""):
    """
    Decorator para cachear respostas de endpoints GET.
    A chave é gerada baseada no prefixo e parâmetros da URL.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Tenta extrair o request dos argumentos
            request = next((arg for arg in args if isinstance(arg, Request)), None)
            if not request:
                request = kwargs.get("request")

            if not request:
                # Se não achar request, roda sem cache
                return await func(*args, **kwargs)

            # Gera chave única: prefixo:url_path
            # Ex: menu:hamburgueria-ze
            # Se o key_prefix tiver {param}, tenta substituir pelos kwargs
            try:
                final_prefix = key_prefix.format(**kwargs)
            except:
                final_prefix = key_prefix

            cache_key = f"{final_prefix}:{request.url.path}"
            
            # 1. Tenta Cache
            cached_data = CacheService.get(cache_key)
            if cached_data:
                # Retorna resposta pronta (FastAPI Response ou JSON direto)
                # Aqui assumimos que o endpoint retorna um Pydantic Model ou Dict,
                # então desserializamos o JSON do cache.
                try:
                    return json.loads(cached_data)
                except:
                    pass

            # 2. Executa Função Real
            response_data = func(*args, **kwargs)
            
            # Suporte a funções async
            if hasattr(response_data, "__await__"):
                response_data = await response_data

            # 3. Salva no Cache (apenas se for dados serializáveis)
            try:
                # Se for Pydantic, converte para dict
                if hasattr(response_data, "model_dump"):
                    data_to_cache = response_data.model_dump(mode='json')
                elif hasattr(response_data, "dict"):
                    data_to_cache = response_data.dict()
                else:
                    data_to_cache = response_data

                CacheService.set(cache_key, json.dumps(data_to_cache, default=str), ttl)
            except Exception as e:
                logger.warning(f"Não foi possível cachear resposta: {e}")

            return response_data
        return wrapper
    return decorator
