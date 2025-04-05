from typing import Any, Dict, List

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


def get_user_artist_profile(user: User) -> ArtistProfile | None:
    """Get the artist profile for a user."""
    try:
        return ArtistProfile.objects.filter(members=user).first()
    except ArtistProfile.DoesNotExist:
        return None


def get_artist_dashboard_data(user: User) -> Dict[str, Any]:
    """
    Get all data needed for the artist dashboard.

    Args:
        user: The user to get dashboard data for

    Returns:
        Dictionary with artist dashboard data
    """
    artist_profile_count = get_user_artists_count(user)
    result: Dict[str, Any] = {"artist_profile_count": artist_profile_count}

    if artist_profile_count == 1:
        # Get the artist profile with prefetched genres
        artist = ArtistProfile.objects.filter(members=user).prefetch_related("genres").first()

        # Get follower count (mock for now)
        follower_count = 0  # This would be calculated from a FanProfile.following relationship

        # Get profile views (mock for now)
        profile_views = 0  # This would be from an analytics system

        # Get recent activities (mock for now)
        recent_activities = [
            {"date": "2023-06-15", "description": "Profile created"},
            # Add more activities as needed
        ]

        result.update(
            {
                "artist": artist,
                "follower_count": follower_count,
                "profile_views": profile_views,
                "recent_activities": recent_activities,
            }
        )
    elif artist_profile_count > 1:
        # Get all artist profiles for the user
        artist_profiles = ArtistProfile.objects.filter(members=user).prefetch_related("genres")
        result["artist_profiles"] = artist_profiles

    return result
