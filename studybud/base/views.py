from django.shortcuts import render
from .models import Room


# Create your views here.

#rooms = [
    #{'id': 1, 'name': 'Lets learn Python'},
    #{'id': 2, 'name': 'Design with me'},
    #{'id': 3, 'name': 'Frontend Development'},
#]

def home(request):
    room = Room.objects.all()
    context = {'rooms': room}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = None
    for i in room:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}        

    return render(request, 'base/room.html', context)

def login(request):
    return render(request, 'login.html')