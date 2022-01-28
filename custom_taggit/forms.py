from django import forms

from colorfield.widgets import ColorWidget

from custom_taggit.models import CustomTag


class TagForm(forms.ModelForm):
    class Meta:
        model = CustomTag
        fields = ("color",)
        widgets = {
            "color": ColorWidget,
        }
