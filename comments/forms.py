from django import forms
from django.forms.models import ModelForm
from django_comments.forms import CommentForm

# from .models import CustomComment


class CustomCommentChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_t = ''
        if obj.content_object:
            full_t = full_t + str(obj.content_type.model) + \
                ' - ' + str(obj.content_object.title) + ' - '
        elif obj.title:
            full_t = obj.title + ' - '
        full_t = full_t + str(obj.comment)[:50]
        return full_t


class CustomCommentForm(CommentForm):
    title = forms.CharField(max_length=200)
    alias_user = forms.CharField(max_length=200, required=False,
                                 help_text="You can add an Alias Name to your comment if you wish to be "
                                           'incognito (note that Moderators can still know it\'s you)',
                                 label="Alias Name")

    class Meta:
        field = ('title', 'alias_user',)

    def check_for_duplicate_comment(self, new):
        return new

    def get_comment_create_data(self, **kwargs):
        # Use the data of the superclass, and add in the title field
        data = super().get_comment_create_data(**kwargs)
        data['title'] = self.cleaned_data['title']
        data['alias_user'] = self.cleaned_data['alias_user']
        return data


class AdminForm(ModelForm):
    pass
    # parent = CustomCommentChoiceField(queryset=CustomComment.objects.all())
