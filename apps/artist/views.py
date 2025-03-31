from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class ArtistProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "pages/artist/profile.html")


class DashboardView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "pages/artist/dashboard.html")
