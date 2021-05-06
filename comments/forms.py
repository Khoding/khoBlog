from django import forms
from django_comments.forms import CommentForm


class CustomCommentForm(CommentForm):
    title = forms.CharField(max_length=300)

    class Meta:
        field = ('title', 'comment',)

    def get_comment_create_data(self, **kwargs):
        # Use the data of the superclass, and add in the title field
        data = super().get_comment_create_data(**kwargs)
        data['title'] = self.cleaned_data['title']
        return data
