from django import forms

from .models import Page


class PageAddForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'page_head', 'content', 'tags', 'description', 'withdrawn',
                  'enable_comments', 'main_page', 'sites',)


class PageEditForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'page_head', 'content', 'tags', 'description', 'withdrawn',
                  'enable_comments', 'main_page', 'slug', 'sites',)


class PageDeleteForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ()
