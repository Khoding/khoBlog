from captcha.fields import CaptchaField
from django import forms

from .models import Post, Comment, Category

from bootstrap_datepicker_plus import DateTimePickerInput


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_title', 'categories',
                  'description', 'body', 'post_image', 'url_post_type', 'url_post_type_name', 'language',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'featured_title': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'categories': forms.SelectMultiple(attrs={'class': 'bg-dark text-light'}),
            'description': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'body': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'url_post_type': forms.URLInput(attrs={'class': 'bg-dark text-light'}),
            'url_post_type_name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'language': forms.Select(attrs={'class': 'bg-dark text-light'}),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_title', 'categories', 'description',
                  'body', 'post_image', 'slug', 'withdrawn', 'featured', 'big', 'published_date', 'url_post_type', 'url_post_type_name', 'language',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'featured_title': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'categories': forms.SelectMultiple(attrs={'class': 'bg-dark text-light'}),
            'description': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'body': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'slug': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'published_date': DateTimePickerInput(format='%d/%m/%Y %H:%M:%S', attrs={'class': 'bg-dark text-light'}),
            'url_post_type': forms.URLInput(attrs={'class': 'bg-dark text-light'}),
            'url_post_type_name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'language': forms.Select(attrs={'class': 'bg-dark text-light'}),
        }


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'withdrawn')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'description': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'withdrawn': forms.CheckboxInput(attrs={'class': 'bg-dark text-light'}),
        }


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'slug', 'withdrawn')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'description': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'slug': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'withdrawn': forms.CheckboxInput(attrs={'class': 'bg-dark text-light'}),
        }


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ('message',)

        widgets = {
            'message': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
        }


class EditPostCommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ('author', 'message',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'message': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
        }


class ARPostCommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ()
