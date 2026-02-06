"""Formularios para el app."""
from django import forms

from .models import PromptModel


class PromptForm(forms.ModelForm):
    """Formulario para Prompt: nombre, tipo documento, instrucciones, variables."""

    variables_texto = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 3,
            "placeholder": '["tema", "objetivos", "poblacion"]',
            "class": "font-mono text-sm",
        }),
        required=False,
        label="Variables requeridas (JSON)",
        help_text="Estas variables generarán automáticamente los campos en el formulario del Paso 3.",
    )

    class Meta:
        model = PromptModel
        fields = ["titulo", "tipo_documento", "contenido", "descripcion", "activo", "recomendado"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.variables_requeridas:
            import json
            self.initial["variables_texto"] = json.dumps(self.instance.variables_requeridas, ensure_ascii=False, indent=2)

    def clean_variables_texto(self):
        import json
        texto = self.cleaned_data.get("variables_texto", "")
        if not texto or not texto.strip():
            return []
        try:
            parsed = json.loads(texto)
            if isinstance(parsed, list):
                return [str(v).strip() for v in parsed if str(v).strip()]
            return []
        except json.JSONDecodeError:
            # Fallback: líneas o comas
            partes = [p.strip() for p in texto.replace(",", "\n").split("\n") if p.strip()]
            return list(dict.fromkeys(partes))

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.variables_requeridas = self.cleaned_data["variables_texto"]
        if commit:
            instance.save()
        return instance
