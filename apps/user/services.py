from dataclasses import dataclass

from django.db.models import QuerySet

from apps.artist.models import Artist
from apps.artist.selectors import get_favorite_artists, get_latest_artists


@dataclass
class HomePageDTO:
    latest_artists: QuerySet[Artist]
    favorite_artists: QuerySet[Artist]


def get_homepage_data() -> HomePageDTO:
    """Get all data needed for the homepage."""
    prefetch = ["genres", "main_genre"]
    return HomePageDTO(
        latest_artists=get_latest_artists(prefetch_related=prefetch),
        favorite_artists=get_favorite_artists(prefetch_related=prefetch),
    )
