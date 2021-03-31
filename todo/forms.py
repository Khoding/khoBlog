from django import forms
from .models import TodoGroup


class TodoForm(forms.Form):
    title = forms.CharField(required=False)
    todo_group = forms.ModelChoiceField(
        queryset=TodoGroup.objects.all(), required=False)
    description = forms.CharField(required=False)
