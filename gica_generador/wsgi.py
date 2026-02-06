"""WSGI config for gica_generador project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gica_generador.settings")

application = get_wsgi_application()
