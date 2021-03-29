from django import forms
from .models import TodoGroup


class TodoForm(forms.Form):
    title = forms.CharField()
    todo_group = forms.ModelChoiceField(queryset=TodoGroup.objects.all())
    description = forms.CharField()
