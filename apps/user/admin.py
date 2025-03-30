from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import FanProfile, User


class EmailAddressInline(admin.TabularInline):  # type: ignore
    model = EmailAddress
    extra = 0
    readonly_fields = ["verified"]
    fields = ("email", "verified", "primary")


@admin.register(User)
class UserAdmin(BaseUserAdmin):  # type: ignore
    list_display = ("email", "full_name", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "full_name")
    ordering = ("email",)
    inlines = [EmailAddressInline]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("full_name",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "password1", "password2"),
            },
        ),
    )


@admin.register(FanProfile)
class FanProfileAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ("user", "created", "modified")
    search_fields = ("user__email", "user__full_name", "bio")
    filter_horizontal = ("following",)
    raw_id_fields = ("user",)
    fieldsets = (
        (None, {"fields": ("user", "bio", "profile_image")}),
        (_("Relationships"), {"fields": ("following",)}),
    )
