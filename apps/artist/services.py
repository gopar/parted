from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from apps.helpers import BaseData, BaseResult

from .models import ArtistProfile, Genre
from .selectors import get_artist_dashboard_data

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


@dataclass(kw_only=True)
class ArtistDashboardResult(BaseResult):
    artist_profile_count: int
    artist: Optional[ArtistProfile] = None
    artist_profiles: Optional[QuerySet[ArtistProfile]] = None
    follower_count: int = 0
    profile_views: int = 0
    recent_activities: List[Dict[str, Any]] = field(default_factory=list)


def get_artist_dashboard(user: User) -> ArtistDashboardResult:
    """
    Get dashboard data for an artist user.

    Args:
        user: The user to get dashboard data for

    Returns:
        ArtistDashboardResult with dashboard data
    """
    dashboard_data = get_artist_dashboard_data(user)

    return ArtistDashboardResult(
        success=True,
        artist_profile_count=dashboard_data["artist_profile_count"],
        artist=dashboard_data.get("artist"),
        artist_profiles=dashboard_data.get("artist_profiles"),
        follower_count=dashboard_data.get("follower_count", 0),
        profile_views=dashboard_data.get("profile_views", 0),
        recent_activities=dashboard_data.get("recent_activities", []),
    )


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
