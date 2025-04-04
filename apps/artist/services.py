from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

from django.contrib.auth import get_user_model
from django.db import transaction

from apps.helpers import BaseData, BaseResult

from .models import ArtistProfile, Genre

if TYPE_CHECKING:
    from apps.user.models import User
else:
    User = get_user_model()


@dataclass
class CreateArtistProfileData(BaseData):
    name: str
    bio: str
    main_genre: Optional[Genre] = None
    genres: Optional[List[Genre]] = None
    website: str = ""
    instagram: str = ""
    twitter: str = ""
    youtube: str = ""


@dataclass(kw_only=True)
class CreateArtistProfileResult(BaseResult):
    artist_profile: Optional[ArtistProfile] = None


@transaction.atomic
def create_artist_profile(user: User, data: CreateArtistProfileData) -> CreateArtistProfileResult:
    """Create a new artist profile for the user"""
    try:
        profile = ArtistProfile.objects.create(
            name=data.name,
            bio=data.bio,
            website=data.website,
            instagram=data.instagram,
            twitter=data.twitter,
            youtube=data.youtube,
            main_genre=data.main_genre,
        )

        # Add the user as a member
        profile.members.add(user)

        if data.genres:
            profile.genres.set(data.genres)

        return CreateArtistProfileResult(
            success=True,
            artist_profile=profile,
            message="Artist profile created successfully!",
        )
    except Exception as e:
        return CreateArtistProfileResult(
            success=False,
            message=f"Failed to create artist profile: {str(e)}",
        )
