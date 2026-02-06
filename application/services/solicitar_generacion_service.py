"""
SolicitarGeneracionService: Orquestador que toma prompt + formato y dispara el Webhook.
"""
from typing import Any, Dict

from domain.entities.formato_tesis import FormatoTesis
from domain.entities.prompt import Prompt
from domain.ports.format_repository import FormatRepository
from domain.ports.generation_webhook_port import GenerationWebhookPort
from domain.ports.prompt_repository import PromptRepository


class SolicitarGeneracionService:
    """
    Orquestador que combina prompt, formato y variables,
    y envía la solicitud al webhook de generación.
    """

    def __init__(
        self,
        prompt_repository: PromptRepository,
        format_repository: FormatRepository,
        webhook_port: GenerationWebhookPort,
    ):
        self._prompt_repository = prompt_repository
        self._format_repository = format_repository
        self._webhook_port = webhook_port

    def solicitar_generacion(
        self,
        prompt_id: int,
        formato_id_externo: str,
        variables: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Toma un prompt (por id), un formato (por id_externo) y variables.
        Construye el contexto con el formato y envía al webhook.
        """
        prompt = self._prompt_repository.obtener_por_id(prompt_id)
        if not prompt:
            return {"error": "Prompt no encontrado", "success": False}

        formato = self._format_repository.obtener_por_id(formato_id_externo)
        if not formato:
            return {"error": "Formato no encontrado", "success": False}

        return self._ejecutar_generacion(prompt, formato, variables)

    def solicitar_generacion_con_entidades(
        self,
        prompt: Prompt,
        formato: FormatoTesis,
        variables: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Versión que recibe directamente las entidades."""
        return self._ejecutar_generacion(prompt, formato, variables)

    def _ejecutar_generacion(
        self,
        prompt: Prompt,
        formato: FormatoTesis,
        variables: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Construye el contexto y envía al webhook."""
        import json

        contexto = json.dumps(
            {
                "formato": formato.estructura_json,
                "universidad": formato.universidad,
            },
            ensure_ascii=False,
        )
        return self._webhook_port.enviar(
            contexto=contexto,
            prompt=prompt.contenido,
            variables=variables,
        )
