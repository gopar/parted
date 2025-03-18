from typing import Any

from django import forms

from apps.user.models import User


class UserProfileForm(forms.Form):
    full_name = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={"class": "input input-bordered w-full"}),
    )
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "textarea textarea-bordered h-24"}))
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "file-input file-input-bordered w-full"}),
    )

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        self.user = user
        initial = kwargs.get("initial", {})
        if not initial and user:
            initial = {
                "full_name": user.full_name or "",
                "bio": user.fan_profile.bio or "",
            }
            if hasattr(user, "fan_profile"):
                initial["bio"] = user.fan_profile.bio
        kwargs["initial"] = initial
        super().__init__(*args, **kwargs)
