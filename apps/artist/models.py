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
    def ordered_by_latest_artists(self) -> models.QuerySet["Artist"]:
        return self.order_by("-created")


class Artist(TimeStampedModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="artist_profiles",
        related_query_name="artist_profile",
        blank=True,
    )
    main_genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name="primary_artists",
        related_query_name="primary_artist",
        null=True,
        blank=True,
    )
    genres = models.ManyToManyField(Genre, related_name="artists", related_query_name="artist", blank=True)

    objects = ArtistQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name
