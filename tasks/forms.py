from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_text']
        widgets = {
            'task_text': forms.TextInput(attrs={
                'placeholder': 'New task…',
                'class': 'task-input'
            })
        }
        labels = {'task_text': ''}
