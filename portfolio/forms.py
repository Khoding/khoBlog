from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'snippet', 'description', 'technology',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'snippet': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'description': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'technology': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
        }
