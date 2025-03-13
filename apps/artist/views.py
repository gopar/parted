from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/artist/profile.html")
