"""
Vistas Django - CBV y funciones.
"""
import json
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from infrastructure.django_app.forms import PromptForm
from infrastructure.django_app.container import (
    get_gestionar_prompts_service,
    get_sincronizar_formatos_service,
    get_solicitar_generacion_service,
)
from infrastructure.django_app.models import FormatoTesisModel, ProyectoModel, PromptModel


# ============ Prompts CRUD ============

class PromptsListView(ListView):
    """Lista de prompts."""
    model = PromptModel
    template_name = "prompts/prompts_list.html"
    context_object_name = "prompts"
    paginate_by = 20


class PromptCreateView(CreateView):
    """Crear prompt."""
    model = PromptModel
    form_class = PromptForm
    template_name = "prompts/prompt_form.html"
    success_url = reverse_lazy("prompts_list")

    def form_valid(self, form):
        messages.success(self.request, "Prompt creado correctamente.")
        return super().form_valid(form)


class PromptUpdateView(UpdateView):
    """Editar prompt."""
    model = PromptModel
    form_class = PromptForm
    template_name = "prompts/prompt_form.html"
    context_object_name = "prompt"
    success_url = reverse_lazy("prompts_list")

    def form_valid(self, form):
        messages.success(self.request, "Prompt actualizado correctamente.")
        return super().form_valid(form)


class PromptDeleteView(DeleteView):
    """Eliminar prompt."""
    model = PromptModel
    success_url = reverse_lazy("prompts_list")
    template_name = "prompts/prompt_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Prompt eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


class PromptApiView(View):
    """API CRUD de prompts para modal (JSON)."""

    def get(self, request, pk=None):
        pk = pk or request.resolver_match.kwargs.get("pk")
        prompts = PromptModel.objects.filter(activo=True)
        if pk:
            p = PromptModel.objects.filter(pk=pk).first()
            if not p:
                return JsonResponse({"error": "No encontrado"}, status=404)
            return JsonResponse({
                "id": p.pk,
                "titulo": p.titulo,
                "tipo_documento": p.tipo_documento,
                "contenido": p.contenido,
                "descripcion": p.descripcion,
                "variables_requeridas": p.variables_requeridas,
                "activo": p.activo,
                "recomendado": p.recomendado,
            })
        return JsonResponse([{
            "id": p.pk,
            "titulo": p.titulo,
            "tipo_documento": p.tipo_documento,
            "descripcion": p.descripcion,
            "variables_requeridas": p.variables_requeridas,
            "recomendado": p.recomendado,
        } for p in prompts], safe=False)

    def post(self, request):
        data = json.loads(request.body) if request.body else {}
        if "variables_requeridas" in data and isinstance(data["variables_requeridas"], list):
            data["variables_texto"] = json.dumps(data["variables_requeridas"], ensure_ascii=False)
        form = PromptForm(data)
        if form.is_valid():
            p = form.save()
            return JsonResponse({"id": p.pk, "success": True})
        return JsonResponse({"errors": form.errors}, status=400)

    def put(self, request, pk=None):
        pk = pk or request.resolver_match.kwargs.get("pk")
        p = PromptModel.objects.filter(pk=pk).first()
        if not p:
            return JsonResponse({"error": "No encontrado"}, status=404)
        data = json.loads(request.body)
        if "variables_requeridas" in data and isinstance(data["variables_requeridas"], list):
            data["variables_texto"] = json.dumps(data["variables_requeridas"], ensure_ascii=False)
        form = PromptForm(data, instance=p)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return JsonResponse({"errors": form.errors}, status=400)

    def delete(self, request, pk=None):
        pk = pk or request.resolver_match.kwargs.get("pk")
        deleted, _ = PromptModel.objects.filter(pk=pk).delete()
        return JsonResponse({"success": deleted > 0})


# ============ Wizard de Generación ============

class WizardGeneracionView(View):
    """Vista paso a paso: elegir formato y enviar a webhook."""

    def get(self, request):
        formatos = FormatoTesisModel.objects.all()
        prompts = PromptModel.objects.filter(activo=True)
        return render(
            request,
            "generador/wizard_generacion.html",
            {"formatos": formatos, "prompts": prompts},
        )


class SolicitarGeneracionApiView(View):
    """API para solicitar generación (POST con Fetch)."""

    def post(self, request):
        try:
            data = json.loads(request.body)
            prompt_id = data.get("prompt_id")
            formato_id_externo = data.get("formato_id_externo")
            variables = data.get("variables", {})
            titulo = data.get("titulo", "")

            if not prompt_id or not formato_id_externo:
                return JsonResponse(
                    {"success": False, "error": "Faltan prompt_id o formato_id_externo"},
                    status=400,
                )

            prompt = PromptModel.objects.filter(pk=prompt_id).first()
            formato = FormatoTesisModel.objects.filter(id_externo=formato_id_externo).first()
            if not prompt or not formato:
                return JsonResponse({"success": False, "error": "Prompt o formato no encontrado"}, status=400)

            # Crear proyecto antes de enviar
            proyecto = ProyectoModel.objects.create(
                titulo=titulo or variables.get("tema", variables.get("titulo", "Sin título")),
                usuario=request.user.username if request.user.is_authenticated else "anon",
                formato=formato_id_externo,
                formato_label=f"{formato.universidad} - {formato.carrera}" if formato.carrera else formato.universidad,
                prompt_usado=str(prompt_id),
                prompt_titulo=prompt.titulo,
                estado="procesando",
                variables=variables,
            )

            service = get_solicitar_generacion_service()
            resultado = service.solicitar_generacion(
                prompt_id=int(prompt_id),
                formato_id_externo=formato_id_externo,
                variables=variables,
            )

            if resultado.get("success"):
                proyecto.tokens_usados = resultado.get("data", {}).get("tokens", 0) or 0
                proyecto.horas_estimadas = min(5.0, proyecto.tokens_usados / 10000)
            else:
                proyecto.estado = "error"
            proyecto.save()

            resultado["proyecto_id"] = proyecto.pk
            return JsonResponse(resultado)
        except (json.JSONDecodeError, ValueError) as e:
            return JsonResponse(
                {"success": False, "error": str(e)},
                status=400,
            )


class DashboardView(View):
    """Panel principal con métricas y generaciones recientes."""

    def get(self, request):
        proyectos = ProyectoModel.objects.all().order_by("-creado_en")[:10]
        total_proyectos = ProyectoModel.objects.count()
        agg = ProyectoModel.objects.aggregate(
            total_horas=Sum("horas_estimadas"),
            total_tokens=Sum("tokens_usados"),
        )
        total_horas = agg["total_horas"] or 0
        total_tokens = agg["total_tokens"] or 0
        return render(
            request,
            "dashboard/dashboard.html",
            {
                "proyectos": proyectos,
                "total_proyectos": total_proyectos,
                "total_horas": round(total_horas, 1),
                "total_tokens": total_tokens,
            },
        )


class HistorialView(ListView):
    """Historial de generaciones."""

    model = ProyectoModel
    template_name = "dashboard/historial.html"
    context_object_name = "proyectos"
    paginate_by = 20
    ordering = ["-creado_en"]


class SincronizarFormatosView(View):
    """Sincroniza formatos desde la API externa."""

    def post(self, request):
        service = get_sincronizar_formatos_service()
        formatos = service.sincronizar()
        messages.success(request, f"Se sincronizaron {len(formatos)} formatos.")
        return redirect("wizard_generacion")
