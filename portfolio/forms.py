from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'snippet', 'description',
                  'technology', 'repository',)

        widgets = {
            'title': forms.TextInput(),
            'snippet': forms.Textarea(),
            'description': forms.Textarea(),
            'technology': forms.Textarea(),
            'repository': forms.Textarea(),
        }
