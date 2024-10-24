from django.shortcuts import render, get_object_or_404, redirect
from .models import Room
from .forms import RoomForm


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
    room = get_object_or_404(Room, id=pk)
    context = {'room': room}        

    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}

    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

def login(request):
    return render(request, 'login.html')