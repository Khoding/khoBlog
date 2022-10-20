from django import forms

from .models import Song


class SongDeleteForm(forms.ModelForm):
    """SongDeleteForm

    A form to delete a Song

    Args:
        forms ([type]): [description]
    """

    class Meta:
        """Meta class for SongDeleteForm ModelForm"""

        model = Song
        fields = ()
