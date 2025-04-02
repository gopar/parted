# mypy: ignore-errors

from http import HTTPStatus

from django.conf import settings
from django.test import Client


class LoginRequiredTestMixin:
    """
    Mixing that checks given view requires login
    """

    def test_login_required(self, client: Client):
        # Given an unauthenticated user
        # When they try to visit URL
        response = client.get(self.URL)

        # Then they should be redirected to the login page
        assert response.status_code == HTTPStatus.FOUND
        assert settings.LOGIN_URL in response.url
