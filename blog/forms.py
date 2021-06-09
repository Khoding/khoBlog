from bootstrap_datepicker_plus import DateTimePickerInput
from captcha.fields import CaptchaField
from django import forms
from django.forms.models import inlineformset_factory

from .models import Category, Comment, Post, PostContent, Series


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_title', 'categories', 'tags', 'series', 'order_in_series',
                  'description', 'body', 'image', 'url_to_article', 'url_to_article_title', 'language',)

        widgets = {
            'title': forms.TextInput(),
            'featured_title': forms.TextInput(),
            'categories': forms.SelectMultiple(),
            'description': forms.Textarea(),
            'body': forms.Textarea(),
            'url_to_article': forms.URLInput(),
            'url_to_article_title': forms.TextInput(),
            'series': forms.Select(),
            'language': forms.Select(),
        }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_title', 'categories', 'tags', 'series', 'order_in_series', 'description',
                  'body', 'image', 'slug', 'withdrawn', 'featuring_state', 'publication_state', 'published_date', 'url_to_article', 'url_to_article_title', 'language',)

        widgets = {
            'title': forms.TextInput(),
            'featured_title': forms.TextInput(),
            'categories': forms.SelectMultiple(),
            'description': forms.Textarea(),
            'body': forms.Textarea(),
            'slug': forms.TextInput(),
            'published_date': DateTimePickerInput(format='%d/%m/%Y %H:%M:%S', ),
            'url_to_article': forms.URLInput(),
            'url_to_article_title': forms.TextInput(),
            'series': forms.Select(),
            'language': forms.Select(),
        }


class PostDeleteForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ()


class CategoryDeleteForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ()


class SeriesDeleteForm(forms.ModelForm):

    class Meta:
        model = Series
        fields = ()


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'description', 'parent', 'withdrawn',)

        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'parent': forms.Select(),
            'withdrawn': forms.CheckboxInput(),
        }


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'description', 'parent', 'slug', 'withdrawn',)

        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'parent': forms.Select(),
            'slug': forms.TextInput(),
            'withdrawn': forms.CheckboxInput(),
        }


class SeriesAddForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ('title', 'description', 'withdrawn')

        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'withdrawn': forms.CheckboxInput(),
        }


class SeriesEditForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ('title', 'description', 'slug', 'withdrawn')

        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'slug': forms.TextInput(),
            'withdrawn': forms.CheckboxInput(),
        }


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ('title', 'body',)

        widgets = {
            'title': forms.TextInput(),
            'body': forms.Textarea(),
        }


class EditPostCommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ('author', 'title', 'body',)

        widgets = {
            'author': forms.TextInput(),
            'title': forms.TextInput(),
            'body': forms.Textarea(),
        }


class ARPostCommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ()


PostContentFormSet = inlineformset_factory(
    Post, PostContent, extra=1, fields=('body', 'body_image', 'body_image_alt',))
