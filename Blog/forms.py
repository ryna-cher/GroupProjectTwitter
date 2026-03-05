from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'avatar')

class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar']

        labels = {
            'username': 'Username',
            'email': 'Email',
            'avatar': 'Avatar'
        }