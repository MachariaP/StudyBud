from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),  # Add URL for registering a new user.

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),

    path('create-room/', views.createRoom, name='create-room'),  # Add URL for creating a new room.
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),  # Add URL for updating a room.
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),  # Add URL for updating a room.

]