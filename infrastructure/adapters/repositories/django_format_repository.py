"""
Adaptador Django para FormatRepository.
Usa el ORM de Django para cumplir con el puerto del dominio.
"""
from typing import List, Optional

from domain.entities.formato_tesis import FormatoTesis
from domain.ports.format_repository import FormatRepository
from infrastructure.django_app.models import FormatoTesisModel


class DjangoFormatRepository(FormatRepository):
    """Implementación del FormatRepository usando Django ORM."""

    def guardar(self, formato: FormatoTesis) -> FormatoTesis:
        """Guarda o actualiza un formato."""
        model, created = FormatoTesisModel.objects.update_or_create(
            id_externo=formato.id_externo,
            defaults={
                "universidad": formato.universidad,
                "estructura_json": formato.estructura_json,
                "carrera": getattr(formato, "carrera", "") or "",
                "version": getattr(formato, "version", "") or "",
                "incluye": getattr(formato, "incluye", "") or "",
            },
        )
        return FormatoTesis(
            id=model.pk,
            id_externo=model.id_externo,
            universidad=model.universidad,
            estructura_json=model.estructura_json,
            carrera=model.carrera or None,
            version=model.version or None,
            incluye=model.incluye or None,
        )

    def obtener_por_id(self, id_externo: str) -> Optional[FormatoTesis]:
        """Obtiene un formato por su id_externo."""
        try:
            model = FormatoTesisModel.objects.get(id_externo=id_externo)
            return FormatoTesis(
                id=model.pk,
                id_externo=model.id_externo,
                universidad=model.universidad,
                estructura_json=model.estructura_json,
                carrera=model.carrera or None,
                version=model.version or None,
                incluye=model.incluye or None,
            )
        except FormatoTesisModel.DoesNotExist:
            return None

    def listar_todos(self) -> List[FormatoTesis]:
        """Lista todos los formatos almacenados."""
        models = FormatoTesisModel.objects.all()
        return [
            FormatoTesis(
                id=m.pk,
                id_externo=m.id_externo,
                universidad=m.universidad,
                estructura_json=m.estructura_json,
                carrera=m.carrera or None,
                version=m.version or None,
                incluye=m.incluye or None,
            )
            for m in models
        ]
