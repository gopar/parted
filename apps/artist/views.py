from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.helpers import AuthenticatedHttpRequest

from .selectors import get_user_artists_count


class ArtistProfileView(LoginRequiredMixin, View):
    def get(self, request: AuthenticatedHttpRequest) -> HttpResponse:
        return render(request, "pages/artist/profile.html")


class DashboardView(LoginRequiredMixin, View):
    def get(self, request: AuthenticatedHttpRequest) -> HttpResponse:
        artist_profile_count = get_user_artists_count(request.user)
        return render(request, "pages/artist/dashboard.html", context={"artist_profile_count": artist_profile_count})
