# chat/urls.py

from django.urls import path
from .views import ChatListView, ChatDetailView, send_message

urlpatterns = [
    path('', ChatListView.as_view(), name='chat_list'),
    path('<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path('<int:chat_id>/send/', send_message, name='send_message'),
]
