from dataclasses import dataclass
from typing import Optional

from django.core.files.images import ImageFile
from django.db import transaction
from django.db.models import QuerySet

from apps.artist.models import Artist
from apps.artist.selectors import get_favorite_artists, get_latest_artists
from apps.helpers import AuthenticatedHttpRequest
from apps.user.models import FanProfile


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


@dataclass
class UpdateProfile:
    full_name: Optional[str]
    bio: Optional[str]
    profile_image: Optional[ImageFile]


@dataclass
class UpdateProfileResult:
    success: bool


@transaction.atomic
def update_profile(request: AuthenticatedHttpRequest, data: UpdateProfile) -> UpdateProfileResult:
    user = request.user

    user.full_name = data.full_name
    user.save()

    fan_profile, created = FanProfile.objects.get_or_create(user=user)
    fan_profile.bio = data.bio or ""

    if data.profile_image:
        fan_profile.profile_image = data.profile_image

    fan_profile.save()

    return UpdateProfileResult(success=True)
