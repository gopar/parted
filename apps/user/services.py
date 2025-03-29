from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from django.db import transaction
from django.db.models import QuerySet

from apps.artist.models import Artist
from apps.artist.selectors import get_favorite_artists, get_latest_artists
from apps.user.models import FanProfile

if TYPE_CHECKING:
    from apps.user.models import User as UserType

User = get_user_model()


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


@dataclass
class DeleteAccountData:
    confirmation: str


@dataclass
class DeleteAccountResult:
    success: bool
    message: str


@transaction.atomic
def delete_account(user: UserType, data: DeleteAccountData) -> DeleteAccountResult:
    """
    Service to handle account deletion with proper validation.
    """
    if data.confirmation.strip().lower() != "delete my account":
        return DeleteAccountResult(
            success=False,
            message="Account deletion failed. Please type 'delete my account' to confirm.",
        )

    # Delete the user account
    user.delete()

    return DeleteAccountResult(
        success=True,
        message="Your account has been successfully deleted. We're sorry to see you go.",
    )


@transaction.atomic
def update_profile(user: UserType, data: UpdateProfile) -> UpdateProfileResult:
    user.full_name = data.full_name
    user.save()

    fan_profile, created = FanProfile.objects.get_or_create(user=user)
    fan_profile.bio = data.bio or ""

    if data.profile_image:
        fan_profile.profile_image = data.profile_image

    fan_profile.save()

    return UpdateProfileResult(success=True)
