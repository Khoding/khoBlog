from captcha.fields import CaptchaField
from django import forms
from django.forms.models import inlineformset_factory
from taggit_selectize.widgets import TagSelectize

from .models import Category, Comment, Post, PostContent, Series
from django_editorjs_fields import EditorJsWidget


class PostCreateForm(forms.ModelForm):
    """PostCreateForm

    A form to create a Post

    Args:
        forms ([type]): [description]
    """

    class Meta:
        model = Post
        fields = (
            "title",
            "featured_title",
            "categories",
            "tags",
            "series",
            "order_in_series",
            "description",
            "body",
            "body_custom",
            "image",
            "url_to_article",
            "url_to_article_title",
            "language",
        )

        widgets = {
            "title": forms.TextInput(),
            "featured_title": forms.TextInput(),
            "categories": forms.SelectMultiple(),
            "tags": TagSelectize(),
            "description": forms.Textarea(),
            "body": forms.Textarea(),
            "url_to_article": forms.URLInput(),
            "url_to_article_title": forms.TextInput(),
            "series": forms.Select(),
            "language": forms.Select(),
            "body_custom": EditorJsWidget(config={"minHeight": 100}),
        }


class PostEditForm(forms.ModelForm):
    """PostEditForm

    A form to edit a Post

    Args:
        forms ([type]): [description]
    """

    pub_date = forms.SplitDateTimeField(
        required=False,
        input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M:%S", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M:%S",
        ),
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "featured_title",
            "categories",
            "tags",
            "series",
            "order_in_series",
            "description",
            "body",
            "body_custom",
            "image",
            "slug",
            "withdrawn",
            "featuring_state",
            "publication_state",
            "pub_date",
            "url_to_article",
            "url_to_article_title",
            "language",
            "is_outdated",
        )

        widgets = {
            "title": forms.TextInput(),
            "featured_title": forms.TextInput(),
            "categories": forms.SelectMultiple(),
            "description": forms.Textarea(),
            "tags": TagSelectize(),
            "body": forms.Textarea(),
            "slug": forms.TextInput(),
            "url_to_article": forms.URLInput(),
            "url_to_article_title": forms.TextInput(),
            "series": forms.Select(),
            "language": forms.Select(),
            "body_custom": EditorJsWidget(config={"minHeight": 100}),
        }


class PostCloneForm(forms.ModelForm):
    """PostCloneForm

    A form to clone a Post

    Args:
        forms ([type]): [description]
    """

    pub_date = forms.SplitDateTimeField(
        required=False,
        input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M:%S", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M:%S",
        ),
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "featured_title",
            "categories",
            "tags",
            "series",
            "order_in_series",
            "description",
            "body",
            "image",
            "withdrawn",
            "featuring_state",
            "publication_state",
            "pub_date",
            "url_to_article",
            "url_to_article_title",
            "language",
            "is_outdated",
        )

        widgets = {
            "title": forms.TextInput(),
            "featured_title": forms.TextInput(),
            "categories": forms.SelectMultiple(),
            "description": forms.Textarea(),
            "tags": TagSelectize(),
            "body": forms.Textarea(),
            "slug": forms.TextInput(),
            "url_to_article": forms.URLInput(),
            "url_to_article_title": forms.TextInput(),
            "series": forms.Select(),
            "language": forms.Select(),
        }


class PostDeleteForm(forms.ModelForm):
    """PostDeleteForm

    A form to delete a Post

    Args:
        forms ([type]): [description]
    """

    class Meta:
        model = Post
        fields = ()


class CategoryDeleteForm(forms.ModelForm):
    """CategoryDeleteForm

    A form to delete a Category

    Args:
        forms ([type]): [description]
    """

    class Meta:
        model = Category
        fields = ()


class SeriesDeleteForm(forms.ModelForm):
    """SeriesDeleteForm

    A form to delete a Series

    Args:
        forms ([type]): [description]
    """

    class Meta:
        model = Series
        fields = ()


class CategoryCreateForm(forms.ModelForm):
    """CategoryCreateForm

    A form to create a Category

    Args:
        forms ([type]): [description]
    """

    class Meta:
        model = Category
        fields = (
            "title",
            "description",
            "parent",
            "withdrawn",
        )

        widgets = {
            "title": forms.TextInput(),
            "description": forms.Textarea(),
            "parent": forms.Select(),
            "withdrawn": forms.CheckboxInput(),
        }


class CategoryEditForm(forms.ModelForm):
    """CategoryEditForm

    A form to edit a Category

    Args:
        forms ([type]): [description]
    """

    class Meta:
        model = Category
        fields = (
            "title",
            "description",
            "parent",
            "slug",
            "withdrawn",
        )

        widgets = {
            "title": forms.TextInput(),
            "description": forms.Textarea(),
            "parent": forms.Select(),
            "slug": forms.TextInput(),
            "withdrawn": forms.CheckboxInput(),
        }


class SeriesCreateForm(forms.ModelForm):
    """SeriesCreateForm

    A form to create a Series

    Args:
        forms ([type]): [description]
    """

    class Meta:
        model = Series
        fields = ("title", "description", "withdrawn")

        widgets = {
            "title": forms.TextInput(),
            "description": forms.Textarea(),
            "withdrawn": forms.CheckboxInput(),
        }


class SeriesEditForm(forms.ModelForm):
    """SeriesEditForm

    A form to edit a Series

    Args:
        forms ([type]): [description]
    """

    class Meta:
        model = Series
        fields = ("title", "description", "slug", "withdrawn")

        widgets = {
            "title": forms.TextInput(),
            "description": forms.Textarea(),
            "slug": forms.TextInput(),
            "withdrawn": forms.CheckboxInput(),
        }


class CommentForm(forms.ModelForm):
    """CommentForm Deprecated

    A form to create Comments

    Args:
        forms ([type]): [description]
    """

    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = (
            "title",
            "body",
        )

        widgets = {
            "title": forms.TextInput(),
            "body": forms.Textarea(),
        }


class EditPostCommentForm(forms.ModelForm):
    """EditPostCommentForm Deprecated

    A form to edit old Comments

    Args:
        forms ([type]): [description]
    """

    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = (
            "author",
            "title",
            "body",
        )

        widgets = {
            "author": forms.TextInput(),
            "title": forms.TextInput(),
            "body": forms.Textarea(),
        }


class ARPostCommentForm(forms.ModelForm):
    """ARPostCommentForm Deprecated

    A form to reply to old comments

    Args:
        forms ([type]): [description]
    """

    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ()


PostContentFormSet = inlineformset_factory(
    Post,
    PostContent,
    extra=1,
    fields=(
        "body",
        "body_image",
        "body_image_alt",
    ),
)
