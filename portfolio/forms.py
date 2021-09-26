from django import forms

from .models import Project


class ProjectAddForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "title",
            "snippet",
            "description",
            "technology",
            "repository",
        )


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("title", "snippet", "description", "technology", "repository", "slug")
