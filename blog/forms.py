from django import forms

from markdownx.fields import MarkdownxFormField

from .models import Post, Comment, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'categories', 'description', 'body', 'post_image')

        body = MarkdownxFormField()

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
            'categories': forms.SelectMultiple(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
            'description': forms.Textarea(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'categories', 'description',
                  'body', 'post_image', 'slug', 'private',)

        body = MarkdownxFormField()

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
            'categories': forms.SelectMultiple(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
            'description': forms.Textarea(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
            'slug': forms.TextInput(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
            'private': forms.CheckboxInput(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
        }


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'private')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
            'description': forms.Textarea(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
            'private': forms.CheckboxInput(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
        }


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'slug', 'private')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
            'description': forms.Textarea(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
            'slug': forms.TextInput(attrs={'class': 'w3-input w3-theme-dark w3-border-0'}),
            'private': forms.CheckboxInput(attrs={'class': 'w3-input w3-theme-dark w3-border-0 w3-border-0'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'message')

        message = MarkdownxFormField()

        widgets = {
            'author': forms.TextInput(attrs={'class': 'w3-input w3-theme-dark w3-border-0 w3-border-0'}),
        }
