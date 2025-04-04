from django import forms

from .models import ArtistProfile, Genre


class ArtistProfileForm(forms.ModelForm):  # type: ignore
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = ArtistProfile
        fields = ["name", "bio", "main_genre", "website", "instagram", "twitter", "youtube"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "bio": forms.Textarea(
                attrs={"class": "textarea textarea-bordered h-32", "placeholder": "Tell your fans about yourself..."}
            ),
            "main_genre": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "website": forms.URLInput(
                attrs={"class": "input input-bordered w-full", "placeholder": "https://yourwebsite.com"}
            ),
            "instagram": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "@username"}),
            "twitter": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "@username"}),
            "youtube": forms.URLInput(
                attrs={"class": "input input-bordered w-full", "placeholder": "https://youtube.com/c/yourchannel"}
            ),
        }
