"""
Container / Factory para inyectar dependencias.
Ensambla adaptadores y servicios.
"""
from django.conf import settings

from application.services.gestionar_prompts_service import GestionarPromptsService
from application.services.sincronizar_formatos_service import SincronizarFormatosService
from application.services.solicitar_generacion_service import SolicitarGeneracionService
from infrastructure.adapters.http.external_format_api_adapter import ExternalFormatApiAdapter
from infrastructure.adapters.http.webhook_adapter import WebhookAdapter
from infrastructure.adapters.repositories.django_format_repository import DjangoFormatRepository
from infrastructure.adapters.repositories.django_prompt_repository import DjangoPromptRepository


def get_gestionar_prompts_service() -> GestionarPromptsService:
    """Factory para GestionarPromptsService."""
    repo = DjangoPromptRepository()
    return GestionarPromptsService(prompt_repository=repo)


def get_sincronizar_formatos_service() -> SincronizarFormatosService:
    """Factory para SincronizarFormatosService."""
    api = ExternalFormatApiAdapter(base_url=getattr(settings, "EXTERNAL_FORMATS_API_URL", ""))
    repo = DjangoFormatRepository()
    return SincronizarFormatosService(external_format_api=api, format_repository=repo)


def get_solicitar_generacion_service() -> SolicitarGeneracionService:
    """Factory para SolicitarGeneracionService."""
    prompt_repo = DjangoPromptRepository()
    format_repo = DjangoFormatRepository()
    webhook = WebhookAdapter(webhook_url=getattr(settings, "WEBHOOK_URL", ""))
    return SolicitarGeneracionService(
        prompt_repository=prompt_repo,
        format_repository=format_repo,
        webhook_port=webhook,
    )
