from django import forms
from taggit_selectize.widgets import TagSelectize

from .models import Page


class PageAddForm(forms.ModelForm):
    """Form for adding a new page"""

    class Meta:
        model = Page
        fields = (
            "title",
            "page_head",
            "content",
            "tags",
            "description",
            "withdrawn",
            "enable_comments",
            "main_page",
            "sites",
        )

        widgets = {
            "tags": TagSelectize(),
        }


class PageEditForm(forms.ModelForm):
    """Form for editing a page"""

    class Meta:
        model = Page
        fields = (
            "title",
            "page_head",
            "content",
            "tags",
            "description",
            "slug",
            "featuring_state",
            "withdrawn",
            "enable_comments",
            "main_page",
            "sites",
        )

        widgets = {
            "tags": TagSelectize(),
        }


class PageDeleteForm(forms.ModelForm):
    """Form for deleting a page"""

    class Meta:
        model = Page
        fields = ()
