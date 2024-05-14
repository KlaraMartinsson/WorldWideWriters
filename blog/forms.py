from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Post, Rating


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','continents', 'post_image', 'excerpt', 'content']

        widgets = {
            "continents": forms.Select(attrs={"class": "form-control"}),
            "content": SummernoteWidget(attrs={"class": "form-control"}),
            "title": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Max 50 characters"}
            ),
            "excerpt": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Max 200 characters"}
            ),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = [
            "rating",
        ]

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
