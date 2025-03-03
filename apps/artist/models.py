from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class Artist(TimeStampedModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="artist_profiles",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name
