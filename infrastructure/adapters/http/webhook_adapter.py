"""
Adaptador Webhook (n8n): Envía datos POST al endpoint de generación.
Implementa GenerationWebhookPort.
"""
from typing import Any, Dict

import requests

from domain.ports.generation_webhook_port import GenerationWebhookPort


class WebhookAdapter(GenerationWebhookPort):
    """
    Envía un POST al webhook n8n con el payload esperado:
    { "contexto": str, "prompt": str, "variables": dict }
    """

    def __init__(self, webhook_url: str):
        self._webhook_url = webhook_url

    def enviar(
        self,
        contexto: str,
        prompt: str,
        variables: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Envía el payload JSON al webhook."""
        payload = {
            "contexto": contexto,
            "prompt": prompt,
            "variables": variables,
        }

        try:
            response = requests.post(
                self._webhook_url,
                json=payload,
                timeout=30,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            resp_data = response.json() if response.content else {}
            # Si n8n devuelve message, lo propagamos
            return {
                "success": True,
                "status_code": response.status_code,
                "data": resp_data,
                "message": resp_data.get("message", "Envío aceptado"),
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None) if hasattr(e, "response") else None,
            }
