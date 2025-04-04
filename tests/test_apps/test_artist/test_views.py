import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

from apps.artist.forms import ArtistProfileForm
from apps.artist.models import ArtistProfile
from factories.artist import artist_create, genre_create
from tests.utils import LoginRequiredTestMixin

User = get_user_model()


@pytest.mark.django_db
class TestArtistProfileView(LoginRequiredTestMixin):
    URL = reverse("artist:profile")

    def test_get_artist_profile_view(self, authenticated_fan_client):
        # When a logged-in user visits the artist profile page
        response = authenticated_fan_client.get(self.URL)

        # Then they should see the artist profile form
        assert response.status_code == 200
        assert "form" in response.context
        assert isinstance(response.context["form"], ArtistProfileForm)
        assert "genres" in response.context
        assert b"Create Your Artist Profile" in response.content

    def test_post_artist_profile_valid_data(self, authenticated_fan_client, user):
        # Given a logged-in user and some genres
        rock_genre = genre_create(name="Rock")
        pop_genre = genre_create(name="Pop")

        # When they submit valid artist profile data
        data = {
            "name": "Test Artist",
            "bio": "This is a test artist bio",
            "main_genre": rock_genre.id,
            "genres": [rock_genre.id, pop_genre.id],
            "website": "https://example.com",
            "instagram": "https://instagram.com/test",
            "twitter": "https://x.com/testartist",
            "youtube": "https://yoytube.com/test",
        }

        response = authenticated_fan_client.post(self.URL, data)

        # Then they should be redirected to the dashboard
        assert response.status_code == 302
        assert response.url == reverse("artist:dashboard")

        # And an artist profile should be created
        assert ArtistProfile.objects.filter(name="Test Artist").exists()
        artist = ArtistProfile.objects.get(name="Test Artist")
        assert artist.bio == "This is a test artist bio"
        assert artist.main_genre == rock_genre
        assert rock_genre in artist.genres.all()
        assert pop_genre in artist.genres.all()
        assert artist.genres.count() == 2
        assert artist.website == "https://example.com"

        # And a success message should be displayed
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert "success" in messages[0].tags

    def test_post_artist_profile_invalid_data(self, authenticated_fan_client):
        # Given a logged-in user
        # When they submit invalid artist profile data (missing required name)
        data = {
            "bio": "This is a test artist bio",
            "website": "https://example.com",
        }

        response = authenticated_fan_client.post(self.URL, data)

        # Then they should see the form with errors
        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["form"].errors
        assert "name" in response.context["form"].errors

        # And no artist profile should be created
        assert not ArtistProfile.objects.exists()


@pytest.mark.django_db
class TestDashboardView(LoginRequiredTestMixin):
    URL = reverse("artist:dashboard")

    def test_dashboard_view_no_artist_profiles(self, authenticated_fan_client):
        # Given a logged-in user with no artist profiles
        # When they visit the dashboard
        response = authenticated_fan_client.get(self.URL)

        # Then they should see the dashboard with artist_profile_count = 0
        assert response.status_code == 200
        assert "artist_profile_count" in response.context
        assert response.context["artist_profile_count"] == 0

    def test_dashboard_view_with_artist_profiles(self, authenticated_fan_client, user):
        # Given a logged-in user with artist profiles
        artist_create(members=[user])
        artist_create(members=[user])

        # When they visit the dashboard
        response = authenticated_fan_client.get(self.URL)

        # Then they should see the dashboard with artist_profile_count = 2
        assert response.status_code == 200
        assert "artist_profile_count" in response.context
        assert response.context["artist_profile_count"] == 2
