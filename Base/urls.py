from django.urls import path
from . import views

urlpatterns= [
    path('login/', views.LoginPage, name="Login" ),
    path('logout/', views.LogoutUser, name="Logout"),
    path('register/', views.RegisterPage, name="Register"),
    path('', views.home, name="Home"),
    path('room/<str:pk>/', views.room, name="Room"),
    path('profile<str:pk>/', views.UserProfile, name="User-Profile"),
    path('create-room/', views.createRoom, name="Create-Room"),
    path('update-room/<str:pk>', views.updateRoom, name="Update-Room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="Delete-Room"),
    path('delete-message/<str:pk>', views.DeleteMessage, name="Delete-Message"),
    path('update-user/', views.UpdateUser, name="Update-User"), 
    path('topics/', views.TopicsPage, name="Topics" ),
    path('activity/', views.ActivityPage, name="Activity")
]