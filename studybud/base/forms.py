from django import forms
from django.forms import ModelForm
from .models import Room, Profile
from django.contrib.auth.models import User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'placeholder': 'Tell others about yourself...',
                'rows': 4,
            }),
        }