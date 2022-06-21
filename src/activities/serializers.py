from rest_framework import serializers

from activities.models import Activity, ACTIVITY_TYPES


def get_choices(choices_given):
    choices_given = serializers.ChoiceField(choices=choices_given).choices
    choices = []
    for choice in choices_given.items():
        value, label = choice
        choices.append({"label": label, "value": value})
    return choices


class ActivitySerializer(serializers.ModelSerializer):
    type_choices = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = (
            "id",
            "description",
            "type",
            "type_choices",
            "number_of_participants",
            "cost",
            "created",
            "is_performed",
        )

    def get_type_choices(self, obj):
        return get_choices(ACTIVITY_TYPES)
