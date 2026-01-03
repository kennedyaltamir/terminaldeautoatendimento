from slowapi import Limiter
from slowapi.util import get_remote_address

# Inicializa o limitador usando o IP do cliente como chave
limiter = Limiter(key_func=get_remote_address)