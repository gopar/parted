from django.http import HttpRequest

from apps.user.models import User


class AuthenticatedHttpRequest(HttpRequest):
    user: User
