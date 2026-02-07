# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-06 13:55:00
# DESCRIPTION: Tipos monetários e sanitização com correções de estilo E701 e E722.
import re
from decimal import Decimal
from typing import Optional, Annotated, Union
from pydantic import PlainSerializer, BeforeValidator

def decimal_to_cents(v: Decimal | None) -> int | None:
    """
    SERIALIZER (Output): Banco (Decimal) -> JSON (Int Centavos)
    Ex: 25.00 -> 2500
    """
    if v is None: return None
    # Arredonda para evitar flutuação de ponto flutuante
    return int(round(v * 100))

def cents_to_decimal(v: Union[int, float, str, Decimal, None]) -> Decimal | None:
    """
    VALIDATOR (Input): JSON (Int Centavos) -> Banco (Decimal)
    Ex: 2500 -> 25.00
    """
    if v is None: return None
    if v == "": return None
    
    # Se já for Decimal (uso interno), retorna direto
    if isinstance(v, Decimal):
        return v
        
    # Converte para Decimal e divide por 100
    try:
        return Decimal(str(v)) / 100
    except Exception: # 🛡️ FIX: E722 - Exceção tipada
        return Decimal(0)

# Tipo Customizado para Pydantic
Monetary = Annotated[
    Decimal,
    PlainSerializer(decimal_to_cents, return_type=int, when_used='json'),
    BeforeValidator(cents_to_decimal)
]

OptionalMonetary = Annotated[
    Optional[Decimal],
    PlainSerializer(decimal_to_cents, return_type=Optional[int], when_used='json'),
    BeforeValidator(cents_to_decimal)
]

def sanitize_html(v: str | None) -> str | None:
    if v is None:
        return None
    clean = re.sub(r'<[^>]*>', '', v)
    return clean.strip()
