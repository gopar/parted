from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from apps.user.services import get_homepage_data


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
