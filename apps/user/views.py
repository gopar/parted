from typing import Any

from allauth.account.views import EmailView as EmailDjangoAllAuthView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from apps.helpers import AuthenticatedHttpRequest
from apps.user.forms import UserProfileForm
from apps.user.services import get_homepage_data

from .services import UpdateProfile, UpdateProfileResult, update_profile


def index(request: HttpRequest) -> HttpResponse:
    template = "pages/index.html"
    if request.user.is_authenticated:
        template = "pages/home_feed.html"

    homepage_data = get_homepage_data()

    return render(
        request,
        template,
        context={
            "latest_artists": homepage_data.latest_artists,
            "favorite_artists": homepage_data.favorite_artists,
        },
    )


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/about.html")


@login_required
def news_feed(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/news_feed.html")


@login_required
def profile(request: AuthenticatedHttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserProfileForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            data = UpdateProfile(**form.cleaned_data)
            result: UpdateProfileResult = update_profile(request, data)

            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = UserProfileForm(request.user)

    return render(request, "pages/profile.html", {"form": form})


@login_required
def settings(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/settings.html")


class EmailView(EmailDjangoAllAuthView):  # type: ignore
    """
    Override django-allauth email view (view to manage emails) to redirect to profile view
    """

    success_url = reverse_lazy("profile")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponseRedirect(self.get_success_url())
