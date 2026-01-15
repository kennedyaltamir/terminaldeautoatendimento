
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 08:00:00
from enum import Enum
from typing import Union, Optional

def normalize_enum(value: Union[str, Enum, None]) -> Optional[str]:
    """
    Normaliza valores de Enum ou String para persistência segura no banco.
    Garante: lowercase, strip e conversão de Enum para value.
    """
    if value is None:
        return None
    
    if isinstance(value, Enum):
        value = value.value
        
    return str(value).lower().strip()

