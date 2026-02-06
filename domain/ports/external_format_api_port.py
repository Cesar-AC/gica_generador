"""
Puerto ExternalFormatApiPort: Para traer formatos de otro sistema.
"""
from abc import ABC, abstractmethod
from typing import List

from domain.entities.formato_tesis import FormatoTesis


class ExternalFormatApiPort(ABC):
    """Interfaz para obtener formatos desde una API externa."""

    @abstractmethod
    def obtener_formatos(self) -> List[FormatoTesis]:
        """Obtiene la lista de formatos desde el sistema externo (GET)."""
        pass
