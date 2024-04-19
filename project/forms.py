# project/forms.py

from django import forms
from .models import Project, TodoTask

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title']

class TodoTaskForm(forms.ModelForm):
    class Meta:
        model = TodoTask
        fields = ['description', 'status']
