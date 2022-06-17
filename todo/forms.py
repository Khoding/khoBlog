from django import forms

from .models import Task


class TaskAddForm(forms.ModelForm):
    """Form for adding a new task"""

    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Add new task...", "class": "mb-2"}))
    description = forms.TextInput(attrs={"class": "mb-2"})

    class Meta:
        """Meta"""

        model = Task
        fields = ("title", "description")


class TaskEditForm(forms.ModelForm):
    """Form for editing a task"""

    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Add new task...", "class": "mb-2"}))
    description = forms.TextInput(attrs={"class": "mb-2"})

    class Meta:
        """Meta"""

        model = Task
        fields = ("title", "description", "withdrawn", "status", "note", "completed_date")


class TaskChangeStatusForm(forms.ModelForm):
    """TaskChangeStatusForm"""

    class Meta:
        """Meta"""

        model = Task
        fields = (
            "status",
            "note",
        )
