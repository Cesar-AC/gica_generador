"""
Puerto GenerationWebhookPort: Para enviar datos a la IA.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class GenerationWebhookPort(ABC):
    """Interfaz para enviar datos al webhook de generación (n8n)."""

    @abstractmethod
    def enviar(
        self,
        contexto: str,
        prompt: str,
        variables: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Envía un POST al webhook con contexto, prompt y variables.
        Retorna la respuesta del webhook.
        """
        pass
