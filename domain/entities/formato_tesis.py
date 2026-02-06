"""
Entidad FormatoTesis del dominio.
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class FormatoTesis:
    """FormatoTesis: id_externo, universidad, estructura_json."""

    id_externo: str
    universidad: str
    estructura_json: Dict[str, Any]
    id: Optional[int] = None
    carrera: Optional[str] = None
    version: Optional[str] = None
    incluye: Optional[str] = None
