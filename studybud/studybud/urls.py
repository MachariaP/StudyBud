
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Home</h1>')

def room(request):
    return HttpResponse('<h1>Room</h1>')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('room/', room),
]
