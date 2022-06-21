from django.urls import path, include
from rest_framework import routers
from activities.views import ActivityViewSet, ActivityGenerateViewSet

router = routers.DefaultRouter()

router.register("activities", ActivityViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("generate/", ActivityGenerateViewSet.as_view()),
]
