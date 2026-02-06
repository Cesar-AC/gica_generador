"""
Modelos de Django para persistencia.
Solo infrastructure conoce django.db.models. El dominio no conoce el ORM.
"""
from django.db import models


class PromptModel(models.Model):
    """Modelo ORM para Prompt."""

    TIPOS_DOCUMENTO = [
        ("tesis_completa", "Tesis Completa"),
        ("resumen_intro", "Solo Resumen/Intro"),
        ("marco_teorico", "Marco Teórico"),
        ("articulo", "Artículo Científico"),
        ("otro", "Otro"),
    ]

    titulo = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=50, choices=TIPOS_DOCUMENTO, default="tesis_completa")
    contenido = models.TextField()
    descripcion = models.CharField(max_length=500, blank=True)
    variables_requeridas = models.JSONField(default=list)  # Lista de strings
    activo = models.BooleanField(default=True)
    recomendado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "gica_prompts"
        verbose_name = "Prompt"
        verbose_name_plural = "Prompts"


class FormatoTesisModel(models.Model):
    """Modelo ORM para FormatoTesis."""

    id_externo = models.CharField(max_length=100, unique=True, db_index=True)
    universidad = models.CharField(max_length=255)
    carrera = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=50, blank=True)
    incluye = models.CharField(max_length=500, blank=True)  # Ej: "Carátula, Índice, Cap 1-4"
    estructura_json = models.JSONField(default=dict)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "gica_formatos_tesis"
        verbose_name = "Formato de Tesis"
        verbose_name_plural = "Formatos de Tesis"


class ProyectoModel(models.Model):
    """Modelo ORM para Proyecto / Generación."""

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("enviado", "Enviado"),
        ("procesando", "Procesando"),
        ("completado", "Completado"),
        ("error", "Error"),
    ]

    titulo = models.CharField(max_length=500, blank=True)
    usuario = models.CharField(max_length=255, default="anon")
    formato = models.CharField(max_length=100)  # id_externo del FormatoTesis
    formato_label = models.CharField(max_length=255, blank=True)
    prompt_usado = models.CharField(max_length=255)
    prompt_titulo = models.CharField(max_length=255, blank=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default="procesando")
    variables = models.JSONField(default=dict, null=True, blank=True)
    tokens_usados = models.PositiveIntegerField(default=0)
    horas_estimadas = models.FloatField(default=0)  # Ahorro de tiempo aproximado
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "gica_proyectos"
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
