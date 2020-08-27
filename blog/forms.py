from django import forms

from .models import Post, Comment, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'categories', 'description', 'body',)


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'categories', 'description',
                  'body', 'slug', 'private',)


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'private')


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'slug', 'private')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'message')
