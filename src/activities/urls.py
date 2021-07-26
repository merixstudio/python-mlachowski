from django.urls import path, include
from rest_framework import routers
from activities.views import ActivityViewSet

router = routers.DefaultRouter()

router.register("activities", ActivityViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
