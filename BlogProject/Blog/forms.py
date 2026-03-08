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

class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'widgets/custom_clearable_file_input.html'

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'avatar': 'Avatar'
        }
        widgets = {
            'avatar': CustomClearableFileInput,
        }