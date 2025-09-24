# base/forms.py

from django.forms import ModelForm
from .models import Room, Topic
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


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name']