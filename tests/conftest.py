import pytest
from allauth.account.models import EmailAddress
from django.test import RequestFactory

from factories.user import user_create


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def user():
    return user_create(email="test@example.com", password="password123")


@pytest.fixture
def verified_user(db, user):
    EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
    return user


@pytest.fixture
def authenticated_client(client, verified_user):
    client.force_login(verified_user)
    return client
