from django.conf import settings
from django.urls import include, path

urlpatterns = []

if settings.DEBUG:

    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns += [
        path("docs/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
        path("docs/redoc/", SpectacularRedocView.as_view(), name="redoc"),
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
    ]
