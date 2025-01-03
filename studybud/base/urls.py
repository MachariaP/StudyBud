from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),  # Add URL for registering a new user.

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),

    path('create-room/', views.createRoom, name='create-room'),  # Add URL for creating a new room.
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),  # Add URL for updating a room.
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),  # Add URL for deleting a room.
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),  # Add URL for deleting a message.

    path('update-user/', views.updateUser, name='update-user'),  # Add URL for updating a user.

    path('topics/', views.topicsPage, name='topics'), # Add URL for topics page.
]