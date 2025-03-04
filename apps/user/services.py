from dataclasses import dataclass

from django.db.models import QuerySet

from apps.artist.models import Artist
from apps.artist.selectors import get_artists_by_genre, get_latest_artists, get_random_artists


@dataclass
class HomePageDTO:
    latest_artists: QuerySet[Artist]
    random_artists: QuerySet[Artist]
    favorite_artists: QuerySet[Artist]
    christian_artists: QuerySet[Artist]


def get_homepage_data() -> HomePageDTO:
    """Get all data needed for the homepage."""
    prefetch = ["genres", "members"]
    return HomePageDTO(
        latest_artists=get_latest_artists(prefetch_related=prefetch),
        random_artists=get_random_artists(prefetch_related=prefetch),
        # For now, random artists are used as favorites
        # This should be replaced with actual favorites logic
        favorite_artists=get_random_artists(prefetch_related=prefetch),
        christian_artists=get_artists_by_genre("Christian", prefetch_related=prefetch),
    )
