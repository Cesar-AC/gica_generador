"""
Entidad Prompt del dominio.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Prompt:
    """Prompt: título, contenido, variables_requeridas, activo."""

    titulo: str
    contenido: str
    variables_requeridas: List[str]
    activo: bool = True
    id: Optional[int] = None
    tipo_documento: Optional[str] = None
    descripcion: Optional[str] = None
    recomendado: bool = False
