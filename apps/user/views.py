from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    mock_artist = {
        "name": "John Doe",
        "profile_image": "https://placehold.co/200x200",
        "main_genre": "Jazz",
    }

    template = "pages/index.html"
    if request.user.is_authenticated:
        template = "pages/home_feed.html"

    return render(request, template, context={"artists": [mock_artist for _ in range(5)]})


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/about.html")
