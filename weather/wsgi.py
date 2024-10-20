from os import environ

from django.core.wsgi import get_wsgi_application

environ.setdefault("DJANGO_SETTINGS_MODULE", "weather.settings")
app = get_wsgi_application()
