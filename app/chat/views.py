from django.shortcuts import render

from django.utils import timezone

from chat.models import ChatMessage, Chat

from django.views.generic.detail import DetailView

from django.views.generic.list import ListView


def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})



class ChatDetailView(DetailView):
    model = Chat
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        queryset = Chat.get_chats_for_user(self.request.user)
        context["chat_list"] = queryset
        return context

class ChatListView(ListView):
    model = Chat
    paginate_by = 10  
    template_name = "chat/index.html"

    def get_queryset(self):
        queryset = Chat.get_chats_for_user(self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context