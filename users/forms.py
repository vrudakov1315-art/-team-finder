from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password']

    def clean(self):
        cd = super().clean()
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Пароли не совпадают')
        return cd

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = self.fields.pop('username')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'phone', 'github_url', 'about']
        widgets = {'about': forms.Textarea(attrs={'rows': 4})}


class CustomPasswordChangeForm(PasswordChangeForm):
    pass
