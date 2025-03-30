from allauth.account.adapter import DefaultAccountAdapter
from django.forms import Form
from django.http import HttpRequest

from apps.user.models import FanProfile, User


class PartedAdapter(DefaultAccountAdapter):  # type: ignore
    def save_user(self, request: HttpRequest, user: User, form: Form, commit: bool = True) -> User:
        user = super().save_user(request, user, form, commit)
        FanProfile.objects.create(user=user)

        return user
