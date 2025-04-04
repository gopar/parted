from typing import List

from faker import Faker

from apps.artist.models import ArtistProfile
from apps.user.models import FanProfile, User

from .utils import Auto

fake = Faker()


def user_create(
    email: str = Auto,
    password: str = "password",
    full_name: str = Auto,
    is_active: bool = True,
    is_staff: bool = False,
) -> User:
    user = User.objects.create(
        email=email or fake.email(),
        full_name=fake.name(),
        is_active=is_active,
        is_staff=is_staff,
    )
    user.set_password(password)
    user.save()
    return user


def fan_create(
    user: User = Auto,
    following: List[ArtistProfile] = Auto,
    bio: str = Auto,
) -> FanProfile:
    user = user or user_create()
    fp = FanProfile.objects.create(
        user=user,
        bio=bio or fake.paragraph(),
    )

    if following:
        fp.following.set(following)

    fp.save()
    return fp
