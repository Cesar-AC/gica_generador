"""URLs del app django_app."""
from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("historial/", views.HistorialView.as_view(), name="historial"),
    path("prompts/", views.PromptsListView.as_view(), name="prompts_list"),
    path("prompts/nuevo/", views.PromptCreateView.as_view(), name="prompt_create"),
    path("prompts/<int:pk>/editar/", views.PromptUpdateView.as_view(), name="prompt_update"),
    path("prompts/<int:pk>/eliminar/", views.PromptDeleteView.as_view(), name="prompt_delete"),
    path("api/prompts/", views.PromptApiView.as_view(), name="api_prompts"),
    path("api/prompts/<int:pk>/", views.PromptApiView.as_view(), name="api_prompt_detail"),
    path("wizard/", views.WizardGeneracionView.as_view(), name="wizard_generacion"),
    path("api/generacion/", views.SolicitarGeneracionApiView.as_view(), name="api_generacion"),
    path("api/sincronizar-formatos/", views.SincronizarFormatosView.as_view(), name="sincronizar_formatos"),
]
