import os
import json
import logging
import redis
from typing import Optional, Any, Callable
from functools import wraps
from fastapi import Request, Response
from decimal import Decimal # Import Decimal para serialização

logger = logging.getLogger("CacheService")

class CacheService:
    _client: Optional[redis.Redis] = None
    _enabled = False

    @classmethod
    def initialize(cls):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            # Tenta conectar com timeout curto para não travar o boot
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
            # Loga o erro mas não impede a execução
            logger.error(f"Erro ao ler cache (key={key}): {e}")
            return None

    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300):
        """
        Define um valor no cache com tempo de expiração (TTL).
        Utiliza json.dumps com default=str para serializar tipos não nativos.
        """
        if not cls._enabled or not cls._client:
            return
        try:
            # Serializa o valor, garantindo compatibilidade com Decimal, datetime, etc.
            serialized_value = json.dumps(value, default=str)
            cls._client.setex(key, ttl, serialized_value)
        except Exception as e:
            logger.error(f"Erro ao gravar cache (key={key}): {e}")

    @classmethod
    def delete(cls, pattern: str):
        """Deleta chaves baseadas em um padrão (ex: menu:*)."""
        if not cls._enabled or not cls._client:
            return
        try:
            keys = cls._client.keys(pattern)
            if keys:
                cls._client.delete(*keys)
                logger.info(f"🧹 Cache limpo: {pattern} ({len(keys)} chaves)")
        except Exception as e:
            logger.error(f"Erro ao limpar cache (pattern={pattern}): {e}")

    @classmethod
    def invalidate_menu(cls, slug: str):
        """Atalho para invalidar o cache do menu de uma empresa específica."""
        cls.delete(f"menu:{slug}")

# Inicializa o serviço de cache assim que o módulo é importado
CacheService.initialize()

def cache_response(ttl: int = 60, key_prefix: str = ""):
    """
    Decorator para cachear respostas de endpoints GET.
    A chave é gerada baseada no prefixo e parâmetros da URL.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Tenta extrair o objeto Request dos argumentos (pode vir como arg ou kwarg)
            request = next((arg for arg in args if isinstance(arg, Request)), None)
            if not request:
                request = kwargs.get("request")

            if not request:
                # Se não houver request, não podemos cachear a URL
                return await func(*args, **kwargs)

            # Monta a chave de cache: prefixo:path_completo_da_url
            try:
                # Formata o prefixo se contiver placeholders dos kwargs
                final_prefix = key_prefix.format(**kwargs) if key_prefix else ""
            except KeyError:
                # Se um placeholder não existir, usa o prefixo como está
                final_prefix = key_prefix if key_prefix else ""

            cache_key = f"{final_prefix}:{request.url.path}"

            # 1. Tenta obter dados do cache
            cached_data_str = CacheService.get(cache_key)
            if cached_data_str:
                try:
                    # Desserializa o JSON do cache
                    cached_data = json.loads(cached_data_str)
                    logger.debug(f"HIT Cache: {cache_key}")
                    return cached_data
                except json.JSONDecodeError:
                    logger.warning(f"Cache corrompido para a chave: {cache_key}")
                except Exception as e:
                    logger.error(f"Erro ao processar cache HIT (key={cache_key}): {e}")

            # Se não achou no cache (MISS)
            logger.debug(f"MISS Cache: {cache_key}")
            
            # Executa a função original
            response_data = func(*args, **kwargs)

            # Trata funções assíncronas
            if hasattr(response_data, "__await__"):
                response_data = await response_data

            # 3. Salva a resposta no cache
            try:
                CacheService.set(cache_key, response_data, ttl)
            except Exception as e:
                logger.warning(f"Não foi possível cachear resposta (key={cache_key}): {e}")

            return response_data
        return wrapper
    return decorator

# Inicializa o serviço de cache ao importar o módulo
CacheService.initialize()
