import typing
from typing import Any, ClassVar

from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from model_utils.models import TimeStampedModel


class UserManager(BaseUserManager["User"]):
    def create_user(self, email: str, password: str | None = None, **extra_fields: dict[str, Any]) -> "User":
        """Create and return a regular user with an email and password"""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", typing.cast(Any, True))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: dict[str, Any]) -> "User":
        """Create and return a superuser with all permissions"""
        extra_fields.setdefault("is_staff", typing.cast(Any, True))
        extra_fields.setdefault("is_superuser", typing.cast(Any, True))

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model that uses email instead of username"""

    first_name = None  # type: ignore
    last_name = None  # type: ignore
    username = None  # type: ignore
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=300, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects: ClassVar[UserManager] = UserManager()  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email


class FanProfile(TimeStampedModel):
    """Stores non-artist user data like favorites and purchases."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="fan_profile",
    )
    # favorite_songs = models.ManyToManyField(
    #     "Song", blank=True, related_name="favorited_by"
    # )
    # purchased_songs = models.ManyToManyField(
    #     "Song", blank=True, related_name="purchased_by"
    # )
    following = models.ManyToManyField("artist.Artist", related_name="followers", blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)

    def __str__(self) -> str:
        return f"Fan profile of {self.user.email}"
