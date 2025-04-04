import random
from typing import List

from faker import Faker

from apps.artist.models import ArtistProfile, Genre
from apps.user.models import User

from .utils import Auto

fake = Faker()


def artist_create(
    name: str = Auto,
    members: User | List[User] = Auto,
    genres: List[str] = Auto,
) -> ArtistProfile:
    if not name:
        name = f"Band {fake.name()}"

    if genres:
        _genres = [genre_create(name=genre) for genre in genres]
    if not genres:
        _genres = [genre_create() for _ in range(3)]

    artist = ArtistProfile.objects.create(name=name, main_genre=_genres[0])
    artist.genres.add(*_genres)

    if isinstance(members, list):
        artist.members.set(members)
    elif isinstance(members, User):
        artist.members.add(members)

    artist.save()
    return artist


def genre_create(
    name: str = "",
) -> Genre:
    genres = ["Christian", "Rock", "Pop", "Folk", "Metal", "Indie", "RnB", "Hip Hop"]

    if not name:
        name = random.choice(genres)

    genre, _ = Genre.objects.get_or_create(name=name)
    return genre
