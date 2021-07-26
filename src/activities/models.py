from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


ACTIVITY_TYPES = (
    (0, _("busywork")),
    (1, _("charity")),
    (2, _("cooking")),
    (3, _("diy")),
    (4, _("education")),
    (5, _("music")),
    (6, _("recreational")),
    (7, _("relaxation")),
    (8, _("social")),
)


class Activity(models.Model):
    description = models.CharField(max_length=500, blank=True, verbose_name=_("Activity description"))
    type = models.PositiveSmallIntegerField(choices=ACTIVITY_TYPES, default=0, verbose_name=_("Activity type"))
    number_of_participants = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("Participants"),
    )
    cost = models.PositiveSmallIntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name=_("Cost"),
        help_text=_(
            "Indicative cost from 1 to 10, where 1 is free and 10 is very expensive"
        ),
    )
    created = models.DateTimeField(auto_now_add=True)
    is_performed = models.BooleanField(
        default=False,
        verbose_name=_("Already performed?"),
    )

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")
        ordering = ("-created",)

    def __str__(self) -> str:
        return self.description[:20]
