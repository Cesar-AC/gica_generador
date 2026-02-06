"""Admin de Django para modelos GICA."""
from django.contrib import admin

from .models import FormatoTesisModel, PromptModel, ProyectoModel


@admin.register(PromptModel)
class PromptAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo_documento", "activo", "recomendado", "creado_en")
    list_filter = ("activo", "tipo_documento")
    search_fields = ("titulo", "contenido", "descripcion")


@admin.register(FormatoTesisModel)
class FormatoTesisAdmin(admin.ModelAdmin):
    list_display = ("id_externo", "universidad", "carrera", "version", "creado_en")
    search_fields = ("id_externo", "universidad", "carrera")


@admin.register(ProyectoModel)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "formato_label", "prompt_titulo", "estado", "tokens_usados", "creado_en")
    list_filter = ("estado",)
