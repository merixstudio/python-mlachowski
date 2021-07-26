from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny

from activities.models import Activity
from activities.serializers import ActivitySerializer


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
