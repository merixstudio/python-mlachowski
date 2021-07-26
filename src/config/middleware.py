from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.http.request import HttpRequest
from django.utils.deprecation import MiddlewareMixin


class HealthCheckMiddleware(MiddlewareMixin):
    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path == f"/{settings.HEALTH_CHECK_PATH}":
            return JsonResponse({"health": "OK"})
        return self.get_response(request)
