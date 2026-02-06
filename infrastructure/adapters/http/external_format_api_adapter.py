"""
Adaptador para obtener formatos desde una API externa (GET).
Implementa ExternalFormatApiPort.
"""
from typing import List

import requests

from domain.entities.formato_tesis import FormatoTesis
from domain.ports.external_format_api_port import ExternalFormatApiPort


class ExternalFormatApiAdapter(ExternalFormatApiPort):
    """
    Obtiene formatos desde un endpoint externo.
    Si EXTERNAL_FORMATS_API_URL está vacío, retorna una lista simulada.
    """

    def __init__(self, base_url: str = ""):
        self._base_url = base_url.rstrip("/")

    def obtener_formatos(self) -> List[FormatoTesis]:
        """Obtiene formatos desde la API externa o simula si no hay URL."""
        if not self._base_url:
            return self._formatos_simulados()

        try:
            response = requests.get(
                f"{self._base_url}/formatos",
                timeout=10,
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            data = response.json()

            # Esperamos una lista o un objeto con clave "formatos"
            items = data if isinstance(data, list) else data.get("formatos", [])
            return [self._parse_formato(item) for item in items]
        except (requests.RequestException, ValueError, KeyError) as e:
            # En caso de error, retornar formatos simulados
            return self._formatos_simulados()

    def _parse_formato(self, item: dict) -> FormatoTesis:
        """Convierte un dict de la API en FormatoTesis."""
        return FormatoTesis(
            id_externo=str(item.get("id_externo", item.get("id", ""))),
            universidad=item.get("universidad", "Desconocida"),
            estructura_json=item.get("estructura_json", item.get("estructura", {})),
            carrera=item.get("carrera"),
            version=item.get("version"),
            incluye=item.get("incluye"),
        )

    def _formatos_simulados(self) -> List[FormatoTesis]:
        """Formatos de ejemplo cuando no hay API configurada."""
        return [
            FormatoTesis(
                id_externo="unt-sistemas-2025",
                universidad="Universidad Nacional de Trujillo",
                estructura_json={
                    "capitulos": ["Introducción", "Marco Teórico", "Metodología", "Resultados", "Conclusiones"],
                    "estilo": "APA 7",
                },
                carrera="Sistemas",
                version="2025.1",
                incluye="Carátula, Índice, Cap 1-4, Ref. APA 7.",
            ),
            FormatoTesis(
                id_externo="upn-ingenieria-2024",
                universidad="Universidad Privada del Norte",
                estructura_json={
                    "capitulos": ["Resumen Ejecutivo", "Realidad Problemática", "Marco Teórico", "Metodología", "Resultados", "Conclusiones"],
                    "estilo": "APA 7",
                },
                carrera="Ingeniería",
                version="2024.B",
                incluye="Resumen Ejecutivo, Realidad Problemática, Marco Teórico...",
            ),
        ]
