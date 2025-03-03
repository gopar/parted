import pytest

from factories import artist_create, fan_create


@pytest.mark.django_db
class TestFanProfile:
    def test_fan_can_follow_multiple_artists(self):
        # Given a fan
        fan = fan_create()

        artist1 = artist_create()
        artist2 = artist_create()
        artist3 = artist_create()

        # When they follow an artist
        fan.following.add(artist1)

        # And a 2nd
        fan.following.add(artist2)

        # And a 3rd
        fan.following.add(artist3)

        # Then we can see all the artist they follow
        assert fan.following.count() == 3
