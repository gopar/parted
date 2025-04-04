from typing import List

from django.db.models import QuerySet
from django.db.models.functions import Random

from apps.artist.models import ArtistProfile, Genre
from apps.user.models import User


def get_latest_artists(count: int = 5, prefetch_related: List[str] | None = None) -> QuerySet[ArtistProfile]:
    """Get the latest artists by creation date."""
    queryset = ArtistProfile.objects.ordered_by_latest_artists()
    if prefetch_related:
        queryset = queryset.prefetch_related(*prefetch_related)
    return queryset[:count]


def get_favorite_artists(count: int = 5, prefetch_related: List[str] | None = None) -> QuerySet[ArtistProfile]:
    """Get the favorite artists by creation date."""
    return ArtistProfile.objects.none()


def get_random_artists(count: int = 5, prefetch_related: List[str] | None = None) -> QuerySet[ArtistProfile]:
    """Get random artists."""
    queryset = ArtistProfile.objects.order_by(Random())
    if prefetch_related:
        queryset = queryset.prefetch_related(*prefetch_related)
    return queryset[:count]


def get_artists_by_genre(
    genre_name: str, count: int = 5, prefetch_related: List[str] | None = None
) -> QuerySet[ArtistProfile]:
    """Get artists by genre name."""
    try:
        genre = Genre.objects.get(name=genre_name)
        queryset = genre.primary_artists.order_by(Random())
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)
        return queryset[:count]
    except Genre.DoesNotExist:
        return ArtistProfile.objects.none()


def get_user_artists_count(user: User) -> int:
    """Get the count of artists associated with a user"""

    return ArtistProfile.objects.filter(members=user).count()
