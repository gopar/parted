import pytest
from allauth.account.models import EmailAddress
from django.test import RequestFactory

from factories.user import fan_create, user_create


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
def fan_user(verified_user):
    fan_create(user=verified_user)
    return verified_user


@pytest.fixture
def authenticated_fan_client(client, fan_user):
    client.force_login(fan_user)
    return client
