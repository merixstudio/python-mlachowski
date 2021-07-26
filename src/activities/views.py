import requests
from django.forms import model_to_dict
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from activities.models import Activity, ACTIVITY_TYPES
from activities.serializers import ActivitySerializer


BORED_API_URL = "https://www.boredapi.com/api/"


class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = (
        "type",
        "number_of_participants",
        "cost",
        "created",
        "is_performed",
    )
    ordering = ("-created",)

    def get_queryset(self):
        is_performed = self.request.query_params.get("is_performed", False)
        return self.queryset.filter(is_performed=is_performed)


class ActivityGenerateViewSet(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        response = requests.get(BORED_API_URL + "activity/")
        generated_activity = response.json()

        for key, value in dict(ACTIVITY_TYPES).items():
            if value == generated_activity["type"]:
                activity_type = key

        activity = Activity(
            description=generated_activity["activity"],
            type=activity_type,
            number_of_participants=generated_activity["participants"],
            cost=int(generated_activity["price"] * 10),
        )
        activity.save()

        return Response(model_to_dict(activity))
