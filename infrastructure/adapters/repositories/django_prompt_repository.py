"""
Adaptador Django para PromptRepository.
Usa el ORM de Django para cumplir con el puerto del dominio.
"""
from typing import List, Optional

from domain.entities.prompt import Prompt
from domain.ports.prompt_repository import PromptRepository
from infrastructure.django_app.models import PromptModel


class DjangoPromptRepository(PromptRepository):
    """Implementación del PromptRepository usando Django ORM."""

    def crear(self, prompt: Prompt) -> Prompt:
        """Crea un nuevo prompt."""
        model = PromptModel.objects.create(
            titulo=prompt.titulo,
            contenido=prompt.contenido,
            variables_requeridas=prompt.variables_requeridas,
            activo=prompt.activo,
            tipo_documento=getattr(prompt, "tipo_documento", None) or "tesis_completa",
            descripcion=getattr(prompt, "descripcion", "") or "",
            recomendado=getattr(prompt, "recomendado", False),
        )
        return self._to_prompt(model)

    def _to_prompt(self, model: PromptModel) -> Prompt:
        return Prompt(
            id=model.pk,
            titulo=model.titulo,
            contenido=model.contenido,
            variables_requeridas=model.variables_requeridas,
            activo=model.activo,
            tipo_documento=model.tipo_documento,
            descripcion=model.descripcion or None,
            recomendado=model.recomendado,
        )

    def obtener_por_id(self, id: int) -> Optional[Prompt]:
        """Obtiene un prompt por su id."""
        try:
            model = PromptModel.objects.get(pk=id)
            return self._to_prompt(model)
        except PromptModel.DoesNotExist:
            return None

    def listar_todos(self, solo_activos: bool = False) -> List[Prompt]:
        """Lista todos los prompts."""
        queryset = PromptModel.objects.all()
        if solo_activos:
            queryset = queryset.filter(activo=True)
        return [self._to_prompt(m) for m in queryset]

    def actualizar(self, prompt: Prompt) -> Prompt:
        """Actualiza un prompt existente."""
        model = PromptModel.objects.get(pk=prompt.id)
        model.titulo = prompt.titulo
        model.contenido = prompt.contenido
        model.variables_requeridas = prompt.variables_requeridas
        model.activo = prompt.activo
        model.tipo_documento = getattr(prompt, "tipo_documento", None) or model.tipo_documento
        model.descripcion = getattr(prompt, "descripcion", None) or ""
        model.recomendado = getattr(prompt, "recomendado", False)
        model.save()
        return self._to_prompt(model)

    def eliminar(self, id: int) -> bool:
        """Elimina un prompt por id."""
        deleted, _ = PromptModel.objects.filter(pk=id).delete()
        return deleted > 0
