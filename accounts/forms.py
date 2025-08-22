from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if field.help_text:
                hint = strip_tags(field.help_text)
                field.widget.attrs.update({
                    'title': hint,
                    'data-hint': hint
                })

                field.help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user




class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username']
        labels = {
            'username': 'Username',
        }
