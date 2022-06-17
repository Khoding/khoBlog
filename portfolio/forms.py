from django import forms

from .models import Project, SubProject


class ProjectAddForm(forms.ModelForm):
    """Form for adding a new project"""

    class Meta:
        """Meta"""

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
    """Form for editing a project"""

    class Meta:
        """Meta"""

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


class ProjectDeleteForm(forms.ModelForm):
    """ProjectDeleteForm

    A form to delete a Project

    Args:
        forms ([type]): [description]
    """

    class Meta:
        """Meta class for ProjectDeleteForm ModelForm"""

        model = Project
        fields = ()


class SubProjectAddForm(forms.ModelForm):
    """Form for adding a new subproject"""

    class Meta:
        """Meta"""

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
    """Form for editing a subproject"""

    class Meta:
        """Meta"""

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
