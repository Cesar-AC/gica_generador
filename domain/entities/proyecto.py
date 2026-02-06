"""
Entidad Proyecto del dominio.
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Proyecto:
    """Proyecto: usuario, formato, prompt_usado, estado."""

    usuario: str
    formato: str  # referencia a id_externo de FormatoTesis
    prompt_usado: str  # referencia a título o id de Prompt
    estado: str
    variables: Optional[Dict[str, Any]] = None
    id: Optional[int] = None
