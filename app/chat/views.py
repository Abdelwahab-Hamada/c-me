# chat/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatMessage

class ChatListView(ListView):
    model = Chat
    template_name = 'chat/chat_list.html'
    context_object_name = 'chats'
    extra_context = {'page_title': 'CME'}

class ChatDetailView(DetailView):
    model = Chat
    template_name = 'chat/chat_detail.html'

@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            ChatMessage.objects.create(chat=chat, sender=request.user, text=message)
    return redirect('chat_detail', pk=chat.pk)
