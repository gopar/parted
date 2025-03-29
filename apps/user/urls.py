from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("news_feed/", views.NewsFeedView.as_view(), name="news-feed"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("accounts/email/", views.EmailView.as_view(), name="account_email"),
    path("accounts/delete/", views.DeleteAccountView.as_view(), name="delete-account"),
]
