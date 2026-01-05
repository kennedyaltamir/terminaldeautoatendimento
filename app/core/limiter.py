from slowapi import Limiter
from slowapi.util import get_remote_address

# Inicializa o limitador usando o IP do cliente como chave
# default_limits aplica uma proteção básica global se a rota não tiver decorador específico
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000/day", "100/hour"]
)