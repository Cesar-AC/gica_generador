"""Crea prompts de ejemplo si no existen."""
from django.core.management.base import BaseCommand

from infrastructure.django_app.models import PromptModel


class Command(BaseCommand):
    help = "Crea prompts de ejemplo"

    def handle(self, *args, **options):
        if PromptModel.objects.exists():
            self.stdout.write("Ya existen prompts. Saltando.")
            return
        prompts = [
            {
                "titulo": "Estructura Completa",
                "tipo_documento": "tesis_completa",
                "contenido": "Actúa como un experto investigador académico. El tema de investigación es: {{tema}}. El objetivo general es: {{objetivo_general}}. La población/objeto de estudio: {{poblacion}}. Variable independiente: {{variable_independiente}}. Por favor, redacta el esqueleto y contenido base para todos los capítulos siguiendo las normas académicas.",
                "descripcion": "Genera el esqueleto y contenido base para todos los capítulos.",
                "variables_requeridas": ["tema", "poblacion", "variable_independiente", "objetivo_general"],
                "recomendado": True,
            },
            {
                "titulo": "Solo Resumen/Intro",
                "tipo_documento": "resumen_intro",
                "contenido": "Actúa como un experto. El tema es: {{tema}}. Genera el resumen ejecutivo y la introducción.",
                "descripcion": "Ideal para iniciar o para papers cortos.",
                "variables_requeridas": ["tema"],
                "recomendado": False,
            },
            {
                "titulo": "Marco Teórico",
                "tipo_documento": "marco_teorico",
                "contenido": "Actúa como un investigador. Tema: {{tema}}. Objetivos: {{objetivos}}. Busca antecedentes y bases teóricas relevantes.",
                "descripcion": "Busca antecedentes y bases teóricas.",
                "variables_requeridas": ["tema", "objetivos"],
                "recomendado": False,
            },
        ]
        for p in prompts:
            PromptModel.objects.create(**p)
        self.stdout.write(self.style.SUCCESS(f"Creados {len(prompts)} prompts de ejemplo."))
