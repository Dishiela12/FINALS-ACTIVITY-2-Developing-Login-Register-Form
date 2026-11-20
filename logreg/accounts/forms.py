from datetime import date

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, label='First Name')
    last_name = forms.CharField(max_length=150, label='Last Name')
    birth_date = forms.DateField(label='Birth Date', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'birth_date', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirmed Password'
        for field in self.fields.values():
            field.help_text = ''
            field.widget.attrs.setdefault('class', 'input')
        self.fields['birth_date'].widget.attrs['max'] = date.today().isoformat()

    def clean_birth_date(self):
        born = self.cleaned_data['birth_date']
        if born > date.today():
            raise forms.ValidationError('Birth date cannot be in the future.')
        return born

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profile.objects.create(user=user, birth_date=self.cleaned_data['birth_date'])
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email/Username',
                               widget=forms.TextInput(attrs={'class': 'input', 'autofocus': True}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'input'}))