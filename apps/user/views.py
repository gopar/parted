from typing import Any

from allauth.account.views import EmailView as EmailDjangoAllAuthView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from apps.helpers import AuthenticatedHttpRequest
from apps.user.forms import UserProfileForm
from apps.user.services import delete_account, get_homepage_data

from .services import DeleteAccountData, DeleteAccountResult, UpdateProfile, UpdateProfileResult, update_profile


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
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


class AboutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "pages/about.html")


class NewsFeedView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "pages/news_feed.html")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request: AuthenticatedHttpRequest) -> HttpResponse:
        form = UserProfileForm(request.user)
        return render(request, "pages/profile.html", {"form": form})

    def post(self, request: AuthenticatedHttpRequest) -> HttpResponse:
        form = UserProfileForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            data = UpdateProfile(**form.cleaned_data)
            _result: UpdateProfileResult = update_profile(request.user, data)

            messages.success(request, "Profile updated successfully!")
            return redirect("profile")

        return render(request, "pages/profile.html", {"form": form})


class SettingsView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "pages/settings.html")


class DeleteAccountView(LoginRequiredMixin, View):
    """
    Handle user account deletion request.
    """

    def post(self, request: AuthenticatedHttpRequest) -> HttpResponse:
        data = DeleteAccountData(confirmation=request.POST.get("confirmation", ""))
        result: DeleteAccountResult = delete_account(request.user, data)

        if result.success:
            messages.success(request, result.message)
            return redirect("index")
        else:
            messages.error(request, result.message)
            return redirect("profile")

    def get(self, request: AuthenticatedHttpRequest) -> HttpResponse:
        return redirect("profile")


class EmailView(EmailDjangoAllAuthView):  # type: ignore
    """
    Override django-allauth email view (view to manage emails) to redirect to profile view
    """

    success_url = reverse_lazy("profile")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponseRedirect(self.get_success_url())
