from django import forms

from .models import Project, SubProject


class ProjectAddForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "title",
            "snippet",
            "description",
            "learned",
            "technology",
            "website",
            "repository",
        )


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "title",
            "snippet",
            "description",
            "learned",
            "technology",
            "website",
            "repository",
            "featured",
            "slug",
        )


class SubProjectAddForm(forms.ModelForm):
    class Meta:
        model = SubProject
        fields = (
            "title",
            "snippet",
            "description",
            "learned",
            "parent_project",
            "link_in_repo",
        )


class SubProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = SubProject
        fields = (
            "title",
            "snippet",
            "description",
            "learned",
            "featured",
            "link_in_repo",
            "slug",
        )
