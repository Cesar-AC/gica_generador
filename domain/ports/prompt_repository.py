"""
Puerto PromptRepository: Para CRUD de prompts.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.prompt import Prompt


class PromptRepository(ABC):
    """Interfaz para CRUD de prompts."""

    @abstractmethod
    def crear(self, prompt: Prompt) -> Prompt:
        """Crea un nuevo prompt."""
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Prompt]:
        """Obtiene un prompt por su id."""
        pass

    @abstractmethod
    def listar_todos(self, solo_activos: bool = False) -> List[Prompt]:
        """Lista todos los prompts."""
        pass

    @abstractmethod
    def actualizar(self, prompt: Prompt) -> Prompt:
        """Actualiza un prompt existente."""
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un prompt por id."""
        pass
