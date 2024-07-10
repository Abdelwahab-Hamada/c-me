from django.shortcuts import render

from django.utils import timezone
from django.views.generic.detail import DetailView

from chat.models import ChatMessage

from django.views.generic.list import ListView


def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})



class ChatDetailView(DetailView):
    model = ChatMessage
    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class ChatListView(ListView):
    model = ChatMessage
    paginate_by = 10  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context