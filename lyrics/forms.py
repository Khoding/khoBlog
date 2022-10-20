from django import forms

from .models import Song, Artist, Genre


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


class ArtistDeleteForm(forms.ModelForm):
    """ArtistDeleteForm

    A form to delete a Artist

    Args:
        forms ([type]): [description]
    """

    class Meta:
        """Meta class for ArtistDeleteForm ModelForm"""

        model = Artist
        fields = ()


class GenreDeleteForm(forms.ModelForm):
    """GenreDeleteForm

    A form to delete a Genre

    Args:
        forms ([type]): [description]
    """

    class Meta:
        """Meta class for GenreDeleteForm ModelForm"""

        model = Genre
        fields = ()
