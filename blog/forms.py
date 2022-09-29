from django import forms
from taggit_selectize.widgets import TagSelectize

from .models import Category, Post, PostCatsLink, Series


class PostCreateForm(forms.ModelForm):
    """PostCreateForm

    A form to create a Post

    Args:
        forms ([type]): [description]
    """

    class Meta:
        """Meta class for PostCreateForm ModelForm"""

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
        input_time_formats=["%H:%M", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M",
        ),
    )

    class Meta:
        """Meta class for PostEditForm ModelForm"""

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
            "slug",
            "withdrawn",
            "needs_reviewing",
            "featuring_state",
            "publication_state",
            "pub_date",
            "url_to_article",
            "url_to_article_title",
            "language",
            "vanity_url",
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


class PostDefineFeaturedCategoryForm(forms.ModelForm):
    """PostDefineFeaturedCategoryForm

    A form to define the featured category of a post
    """

    # This just sets the widget type, the queryset is required, so we give everything (a bit slow, but again, once a week action)
    # Find a way to set the queryset to nothing or whatever
    featured_cat = forms.ModelChoiceField(queryset=Category.objects.all())

    def __init__(self, **kwargs):
        # We get the post
        self.post = kwargs.pop("post")
        super(PostDefineFeaturedCategoryForm, self).__init__(**kwargs)
        # And then reset the featured_cat field with only the categories of the post
        self.fields["featured_cat"].queryset = Category.objects.filter(postcatslink__post=self.post)

    class Meta:
        """Meta class for UpdateView ModelForm"""

        model = PostCatsLink
        fields = ("featured_cat",)


class PostCloneForm(forms.ModelForm):
    """PostCloneForm

    A form to clone a Post

    Args:
        forms ([type]): [description]
    """

    pub_date = forms.SplitDateTimeField(
        required=False,
        input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M",
        ),
    )

    class Meta:
        """Meta class for PostCloneForm ModelForm"""

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


class PostMarkOutdatedForm(forms.ModelForm):
    """PostMarkOutdatedForm

    A form to mark a Post as outdated

    Args:
        forms ([type]): [description]
    """

    is_content_outdated_date = forms.SplitDateTimeField(
        required=False,
        input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M",
        ),
    )

    class Meta:
        """Meta class for PostMarkOutdatedForm ModelForm"""

        model = Post
        fields = ("is_content_outdated", "is_content_outdated_date")


class PostDeleteForm(forms.ModelForm):
    """PostDeleteForm

    A form to delete a Post

    Args:
        forms ([type]): [description]
    """

    class Meta:
        """Meta class for PostDeleteForm ModelForm"""

        model = Post
        fields = ()


class CategoryDeleteForm(forms.ModelForm):
    """CategoryDeleteForm

    A form to delete a Category

    Args:
        forms ([type]): [description]
    """

    class Meta:
        """Meta class for CategoryDeleteForm ModelForm"""

        model = Category
        fields = ()


class SeriesDeleteForm(forms.ModelForm):
    """SeriesDeleteForm

    A form to delete a Series

    Args:
        forms ([type]): [description]
    """

    class Meta:
        """Meta class for SeriesDeleteForm ModelForm"""

        model = Series
        fields = ()


class CategoryCreateForm(forms.ModelForm):
    """CategoryCreateForm

    A form to create a Category

    Args:
        forms ([type]): [description]
    """

    class Meta:
        """Meta class for CategoryCreateForm ModelForm"""

        model = Category
        fields = (
            "title",
            "suffix",
            "description",
            "parent",
            "withdrawn",
        )

        widgets = {
            "title": forms.TextInput(),
            "suffix": forms.TextInput(),
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
        """Meta class for CategoryEditForm ModelForm"""

        model = Category
        fields = (
            "title",
            "suffix",
            "description",
            "parent",
            "slug",
            "withdrawn",
            "needs_reviewing",
        )

        widgets = {
            "title": forms.TextInput(),
            "suffix": forms.TextInput(),
            "description": forms.Textarea(),
            "parent": forms.Select(),
            "slug": forms.TextInput(),
            "withdrawn": forms.CheckboxInput(),
            "needs_reviewing": forms.CheckboxInput(),
        }


class SeriesCreateForm(forms.ModelForm):
    """SeriesCreateForm

    A form to create a Series

    Args:
        forms ([type]): [description]
    """

    class Meta:
        """Meta class for SeriesCreateForm ModelForm"""

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
        """Meta class for SeriesEditForm ModelForm"""

        model = Series
        fields = (
            "title",
            "description",
            "slug",
            "withdrawn",
            "needs_reviewing",
        )

        widgets = {
            "title": forms.TextInput(),
            "description": forms.Textarea(),
            "slug": forms.TextInput(),
            "withdrawn": forms.CheckboxInput(),
            "needs_reviewing": forms.CheckboxInput(),
        }
