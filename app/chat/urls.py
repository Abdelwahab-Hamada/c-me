from django.urls import path

from . import views

from .views import ChatDetailView, ChatListView, UserListView, upload_file, create_chat

urlpatterns = [
    path("", ChatListView.as_view(), name="index"),
    path('upload/', upload_file, name='file-upload'),
    path('users/', UserListView.as_view(), name='users-list'),
    path('create/<slug:pk>/', create_chat, name='chat'),
    path("<slug:pk>/", ChatDetailView.as_view(), name="room"),
]