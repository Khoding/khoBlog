from captcha.fields import CaptchaField
from django import forms
from django.forms.models import inlineformset_factory

from .models import Post, Comment, Category, PostContent, Series

from bootstrap_datepicker_plus import DateTimePickerInput


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_title', 'categories', 'tags', 'series', 'post_order_in_series',
                  'description', 'body', 'post_image', 'url_post_type', 'url_post_type_name', 'language',)

        widgets = {
            'title': forms.TextInput(),
            'featured_title': forms.TextInput(),
            'categories': forms.SelectMultiple(),
            'description': forms.Textarea(),
            'body': forms.Textarea(),
            'url_post_type': forms.URLInput(),
            'url_post_type_name': forms.TextInput(),
            'series': forms.Select(),
            'language': forms.Select(),
        }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_title', 'categories', 'tags', 'series', 'post_order_in_series', 'description',
                  'body', 'post_image', 'slug', 'withdrawn', 'featuring_state', 'publication_state', 'published_date', 'url_post_type', 'url_post_type_name', 'language',)

        widgets = {
            'title': forms.TextInput(),
            'featured_title': forms.TextInput(),
            'categories': forms.SelectMultiple(),
            'description': forms.Textarea(),
            'body': forms.Textarea(),
            'slug': forms.TextInput(),
            'published_date': DateTimePickerInput(format='%d/%m/%Y %H:%M:%S', ),
            'url_post_type': forms.URLInput(),
            'url_post_type_name': forms.TextInput(),
            'series': forms.Select(),
            'language': forms.Select(),
        }


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'description', 'withdrawn')

        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'withdrawn': forms.CheckboxInput(),
        }


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'description', 'slug', 'withdrawn')

        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
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
    Post, PostContent, extra=1, fields=('body', 'post_body_image', 'post_body_image_alt',))
