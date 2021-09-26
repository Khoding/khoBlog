from django import forms
from taggit_selectize.widgets import TagSelectize

from .models import Page


class PageAddForm(forms.ModelForm):
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
            "slug",
            "sites",
        )

        widgets = {
            "tags": TagSelectize(),
        }


class PageDeleteForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ()
