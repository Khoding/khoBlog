from django import forms

from .models import FlatPage


class FlatPageAddForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        fields = ('title', 'page_head', 'content', 'description',
                  'enable_comments', 'main_page', 'sites',)


class FlatPageEditForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        fields = ('title', 'page_head', 'content', 'description',
                  'enable_comments', 'main_page', 'slug', 'sites',)
