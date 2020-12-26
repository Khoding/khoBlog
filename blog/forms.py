from django import forms

from .models import Post, Comment, Category

from bootstrap_datepicker_plus import DateTimePickerInput


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_title', 'categories',
                  'description', 'body', 'post_image', 'url_post_type', 'url_post_type_name')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'featured_title': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'categories': forms.SelectMultiple(attrs={'class': 'bg-dark text-light'}),
            'description': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'body': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'url_post_type': forms.URLInput(attrs={'class': 'bg-dark text-light'}),
            'url_post_type_name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_title', 'categories', 'description',
                  'body', 'post_image', 'slug', 'private', 'featured', 'big', 'published_date', 'url_post_type', 'url_post_type_name')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'featured_title': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'categories': forms.SelectMultiple(attrs={'class': 'bg-dark text-light'}),
            'description': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'body': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'slug': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'published_date': DateTimePickerInput(format='%d/%m/%Y %H:%M', attrs={'class': 'bg-dark text-light'}),
            'url_post_type': forms.URLInput(attrs={'class': 'bg-dark text-light'}),
            'url_post_type_name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
        }


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'private')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'description': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'private': forms.CheckboxInput(attrs={'class': 'bg-dark text-light'}),
        }


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'slug', 'private')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'description': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'slug': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'private': forms.CheckboxInput(attrs={'class': 'bg-dark text-light'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)

        widgets = {
            'message': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
        }


class EditPostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'message',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'message': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
        }
