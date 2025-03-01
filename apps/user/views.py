from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "base/index.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "base/about.html")
