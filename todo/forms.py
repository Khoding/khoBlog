from django import forms

from .models import Task


class TaskAddForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Add new task...", "class": "mb-2"}))
    description = forms.TextInput(attrs={"class": "mb-2"})

    class Meta:
        model = Task
        fields = ("title", "description")


class TaskEditForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Add new task...", "class": "mb-2"}))
    description = forms.TextInput(attrs={"class": "mb-2"})

    class Meta:
        model = Task
        fields = ("title", "description", "withdrawn", "status", "reason_of_status", "completed_date")


class TaskChangeStatusForm(forms.ModelForm):
    """TaskChangeStatusForm"""

    class Meta:
        model = Task
        fields = (
            "status",
            "reason_of_status",
        )
