from django import forms

from colorfield.widgets import ColorWidget

from custom_taggit.models import CustomTag


class TagForm(forms.ModelForm):
    """Form for CustomTag"""

    class Meta:
        """Meta"""

        model = CustomTag
        fields = ("color",)
        widgets = {
            "color": ColorWidget,
        }
