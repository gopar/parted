from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("news_feed/", views.news_feed, name="news-feed"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("accounts/email/", views.EmailView.as_view(), name="account_email"),
]
