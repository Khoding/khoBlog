from django import forms
from django_comments_xtd.forms import XtdCommentForm


class CustomCommentXTDForm(XtdCommentForm):
    """Custom comment form"""

    title = forms.CharField(max_length=200, required=False)

    class Meta:
        """Meta"""

        field = "__all__"

    def check_for_duplicate_comment(self, new):
        """Check for duplicate comment"""
        return new

    def get_comment_create_data(self, **kwargs):
        """Get comment create data"""
        # Use the data of the superclass, and add in the title field
        data = super().get_comment_create_data(**kwargs)
        data["title"] = self.cleaned_data["title"]
        return data
