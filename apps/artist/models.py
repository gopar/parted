from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class Genre(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class ArtistQuerySet(models.QuerySet["Artist"]):
    def with_latest_artists(self) -> models.QuerySet["Artist"]:
        """
        Returns the latest n artists by creation date
        """
        return self.order_by("-created")


class Artist(TimeStampedModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="artist_profiles",
        blank=True,
    )
    main_genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name="primary_artists",
        null=True,
        blank=True,
    )
    genres = models.ManyToManyField(Genre, related_name="artists", blank=True)

    objects = ArtistQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name
