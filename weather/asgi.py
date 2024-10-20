from os import environ

from django.core.asgi import get_asgi_application

environ.setdefault("DJANGO_SETTINGS_MODULE", "weather.settings")
app = get_asgi_application()
