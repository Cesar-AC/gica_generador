"""
Puerto FormatRepository: Para guardar/leer formatos.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.formato_tesis import FormatoTesis


class FormatRepository(ABC):
    """Interfaz para persistencia de formatos de tesis."""

    @abstractmethod
    def guardar(self, formato: FormatoTesis) -> FormatoTesis:
        """Guarda o actualiza un formato."""
        pass

    @abstractmethod
    def obtener_por_id(self, id_externo: str) -> Optional[FormatoTesis]:
        """Obtiene un formato por su id_externo."""
        pass

    @abstractmethod
    def listar_todos(self) -> List[FormatoTesis]:
        """Lista todos los formatos almacenados."""
        pass
