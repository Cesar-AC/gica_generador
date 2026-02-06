"""
GestionarPromptsService: Lógica para crear/editar prompts.
"""
from typing import List, Optional

from domain.entities.prompt import Prompt
from domain.ports.prompt_repository import PromptRepository


class GestionarPromptsService:
    """Servicio para gestionar prompts (CRUD)."""

    def __init__(self, prompt_repository: PromptRepository):
        self._prompt_repository = prompt_repository

    def crear_prompt(
        self,
        titulo: str,
        contenido: str,
        variables_requeridas: List[str],
        activo: bool = True,
    ) -> Prompt:
        """Crea un nuevo prompt."""
        prompt = Prompt(
            titulo=titulo,
            contenido=contenido,
            variables_requeridas=variables_requeridas,
            activo=activo,
        )
        return self._prompt_repository.crear(prompt)

    def actualizar_prompt(
        self,
        id: int,
        titulo: Optional[str] = None,
        contenido: Optional[str] = None,
        variables_requeridas: Optional[List[str]] = None,
        activo: Optional[bool] = None,
    ) -> Optional[Prompt]:
        """Actualiza un prompt existente."""
        prompt = self._prompt_repository.obtener_por_id(id)
        if not prompt:
            return None
        if titulo is not None:
            prompt.titulo = titulo
        if contenido is not None:
            prompt.contenido = contenido
        if variables_requeridas is not None:
            prompt.variables_requeridas = variables_requeridas
        if activo is not None:
            prompt.activo = activo
        return self._prompt_repository.actualizar(prompt)

    def obtener_prompt(self, id: int) -> Optional[Prompt]:
        """Obtiene un prompt por id."""
        return self._prompt_repository.obtener_por_id(id)

    def listar_prompts(self, solo_activos: bool = False) -> List[Prompt]:
        """Lista todos los prompts."""
        return self._prompt_repository.listar_todos(solo_activos=solo_activos)

    def eliminar_prompt(self, id: int) -> bool:
        """Elimina un prompt."""
        return self._prompt_repository.eliminar(id)
