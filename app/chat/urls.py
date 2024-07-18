from django.urls import path

from . import views

from .views import ChatDetailView, ChatListView, UserListView, upload_file, create_chat, messages_history, unread_messages
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("", login_required(ChatListView.as_view()), name="index"),
    path('upload/', upload_file, name='file-upload'),
    path('users/', login_required(UserListView.as_view()), name='users-list'),
    path('create/<slug:pk>/', create_chat, name='chat'),
    path('messages/<slug:pk>/', messages_history, name='chat-messages'),
    path('messages/unread/<slug:pk>/', unread_messages, name='unread-messages'),
    path("<slug:pk>/", login_required(ChatDetailView.as_view()), name="room"),
]