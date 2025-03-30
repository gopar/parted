# mypy: ignore-errors
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.user.forms import UserProfileForm

User = get_user_model()


class TestIndexView:
    def test_index_view_unauthenticated(self, client):
        # Given an unauthenticated user
        # When they visit the index page
        response = client.get(reverse("index"))

        # Then they should see the index page
        assert response.status_code == 200
        assert "pages/index.html" in [t.name for t in response.templates]

    @pytest.mark.django_db
    def test_index_view_authenticated(self, authenticated_fan_client):
        # Given an authenticated user
        # When they visit the index page
        response = authenticated_fan_client.get(reverse("index"))

        # Then they should see the home feed page
        assert response.status_code == 200
        assert "pages/home_feed.html" in [t.name for t in response.templates]
        assert "latest_artists" in response.context
        assert "favorite_artists" in response.context


class TestAboutView:
    def test_about_view(self, client):
        # Given any user
        # When they visit the about page
        response = client.get(reverse("about"))

        # Then they should see the about page
        assert response.status_code == 200
        assert "pages/about.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestNewsFeedView:
    def test_news_feed_view_authenticated(self, authenticated_fan_client):
        # Given an authenticated user
        # When they visit the news feed page
        response = authenticated_fan_client.get(reverse("news-feed"))

        # Then they should see the news feed page
        assert response.status_code == 200
        assert "pages/news_feed.html" in [t.name for t in response.templates]

    def test_news_feed_view_unauthenticated(self, client):
        # Given an unauthenticated user
        # When they try to visit the news feed page
        response = client.get(reverse("news-feed"))

        # Then they should be redirected to the login page
        assert response.status_code == 302
        assert "/accounts/login/" in response.url


@pytest.mark.django_db
class TestProfileView:
    def test_profile_view_get(self, authenticated_fan_client):
        # Given an authenticated user
        # When they visit the profile page
        response = authenticated_fan_client.get(reverse("profile"))

        # Then they should see the profile page with a form
        assert response.status_code == 200
        assert "pages/profile.html" in [t.name for t in response.templates]
        assert isinstance(response.context["form"], UserProfileForm)

    def test_profile_view_post_valid(self, authenticated_fan_client, user):
        # Given an authenticated user

        # When they submit valid profile data
        data = {
            "full_name": "Test User",
            "bio": "This is a test bio",
        }
        response = authenticated_fan_client.post(reverse("profile"), data)

        # Then they should be redirected to the profile page
        assert response.status_code == 302
        assert response.url == reverse("profile")

        user.refresh_from_db()
        assert user.full_name == data["full_name"]
        assert user.fan_profile.bio == data["bio"]

    def test_profile_view_post_invalid(self, authenticated_fan_client, verified_user):
        # Given an authenticated user
        # When they submit invalid profile data
        # Note: We're not providing any data, which should make the form invalid
        response = authenticated_fan_client.post(reverse("profile"), {}, follow=True)

        # Then they should see the profile page with form errors
        assert response.status_code == 200
        assert "pages/profile.html" in [t.name for t in response.templates]
        assert "form" in response.context
        assert not response.context["form"].is_valid()


@pytest.mark.django_db
class TestSettingsView:
    def test_settings_view_authenticated(self, authenticated_fan_client):
        # Given an authenticated user
        # When they visit the settings page
        response = authenticated_fan_client.get(reverse("settings"))

        # Then they should see the settings page
        assert response.status_code == 200
        assert "pages/settings.html" in [t.name for t in response.templates]

    def test_settings_view_unauthenticated(self, client):
        # Given an unauthenticated user
        # When they try to visit the settings page
        response = client.get(reverse("settings"))

        # Then they should be redirected to the login page
        assert response.status_code == 302
        assert "/accounts/login/" in response.url


@pytest.mark.django_db
class TestDeleteAccountView:
    def test_delete_account_view_get(self, authenticated_fan_client):
        # Given an authenticated user
        # When they make a GET request to the delete account endpoint
        response = authenticated_fan_client.get(reverse("delete-account"))

        # Then they should be redirected to the profile page
        assert response.status_code == 302
        assert response.url == reverse("profile")

    def test_delete_account_view_post_success(self, authenticated_fan_client, user):
        # Given an authenticated user
        # When they request their account be deleted
        response = authenticated_fan_client.post(reverse("delete-account"), {"confirmation": "delete my account"})

        # Then they should be redirected to the index page
        assert response.status_code == 302
        assert response.url == reverse("index")

        # And the accout is deleted
        with pytest.raises(User.DoesNotExist):
            User.objects.get(id=user.id)

    def test_delete_account_view_post_failure(self, authenticated_fan_client, user):
        # Given an authenticated user
        # When they request their account be delete incorrectly
        response = authenticated_fan_client.post(reverse("delete-account"), {"confirmation": "pikachu"})

        # Then they should be redirected to the profile page
        assert response.status_code == 302
        assert response.url == reverse("profile")

        assert User.objects.get(id=user.id)


@pytest.mark.django_db
class TestEmailView:
    def test_email_view_get(self, authenticated_fan_client):
        # Given an authenticated user
        # When they visit the email view
        response = authenticated_fan_client.get(reverse("account_email"))

        # Then they should be redirected to the profile page
        assert response.status_code == 302
        assert response.url == reverse("profile")
