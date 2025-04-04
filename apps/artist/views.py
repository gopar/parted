from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.helpers import AuthenticatedHttpRequest

from .forms import ArtistProfileForm
from .models import Genre
from .selectors import get_user_artists_count
from .services import CreateArtistProfileData, create_artist_profile


class ArtistProfileView(LoginRequiredMixin, View):
    def get(self, request: AuthenticatedHttpRequest) -> HttpResponse:
        form = ArtistProfileForm()
        genres = Genre.objects.all()
        return render(request, "pages/artist/profile.html", {"form": form, "genres": genres})

    def post(self, request: AuthenticatedHttpRequest) -> HttpResponse:
        form = ArtistProfileForm(request.POST)

        if form.is_valid():
            data = CreateArtistProfileData(
                name=form.cleaned_data["name"],
                bio=form.cleaned_data["bio"],
                main_genre=form.cleaned_data.get("main_genre"),
                genres=form.cleaned_data.get("genres", []),
                website=form.cleaned_data.get("website", ""),
                instagram=form.cleaned_data.get("instagram", ""),
                twitter=form.cleaned_data.get("twitter", ""),
                youtube=form.cleaned_data.get("youtube", ""),
            )

            result = create_artist_profile(request.user, data)

            if result.success:
                messages.success(request, result.message)
                return redirect("artist:dashboard")
            else:
                messages.error(request, result.message)

        # If form is invalid or service failed
        genres = Genre.objects.all()
        return render(request, "pages/artist/profile.html", {"form": form, "genres": genres})


class DashboardView(LoginRequiredMixin, View):
    def get(self, request: AuthenticatedHttpRequest) -> HttpResponse:
        artist_profile_count = get_user_artists_count(request.user)
        return render(request, "pages/artist/dashboard.html", context={"artist_profile_count": artist_profile_count})
