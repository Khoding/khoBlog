from django import forms
from django_comments.forms import CommentForm


class CustomCommentForm(CommentForm):
    title = forms.CharField(max_length=200)
    alias_user = forms.CharField(max_length=200, required=False, help_text="You can add an Alias Name to your comment if you wish to be "
                                 'incognito (note that Moderators can still know it\'s you)', label="Alias Name")

    class Meta:
        field = ('title', 'alias_user',)

    def get_comment_create_data(self, **kwargs):
        # Use the data of the superclass, and add in the title field
        data = super().get_comment_create_data(**kwargs)
        data['title'] = self.cleaned_data['title']
        data['alias_user'] = self.cleaned_data['alias_user']
        return data
