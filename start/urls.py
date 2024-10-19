from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from start.settings import DEBUG, STATIC_ROOT, STATIC_URL

urlpatterns = [
    path("", include("polls.urls")),
    path("admin/", admin.site.urls),
]


if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
