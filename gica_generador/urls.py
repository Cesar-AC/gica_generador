"""URL principal del proyecto."""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

def home(request):
    return redirect("dashboard")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("", include("infrastructure.django_app.urls")),
]
