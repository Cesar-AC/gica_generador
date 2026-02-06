"""
SincronizarFormatosService: Lógica para traer formatos de la API externa.
"""
from typing import List

from domain.entities.formato_tesis import FormatoTesis
from domain.ports.external_format_api_port import ExternalFormatApiPort
from domain.ports.format_repository import FormatRepository


class SincronizarFormatosService:
    """Servicio para sincronizar formatos desde la API externa hacia el repositorio local."""

    def __init__(
        self,
        external_format_api: ExternalFormatApiPort,
        format_repository: FormatRepository,
    ):
        self._external_api = external_format_api
        self._format_repository = format_repository

    def sincronizar(self) -> List[FormatoTesis]:
        """
        Obtiene formatos de la API externa y los guarda en el repositorio local.
        Retorna la lista de formatos sincronizados.
        """
        formatos_externos = self._external_api.obtener_formatos()
        formatos_guardados = []
        for formato in formatos_externos:
            formato_guardado = self._format_repository.guardar(formato)
            formatos_guardados.append(formato_guardado)
        return formatos_guardados
