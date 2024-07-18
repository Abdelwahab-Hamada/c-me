from django.shortcuts import render

from django.utils import timezone

from chat.models import ChatMessage, Chat, MessageAttachment

from django.views.generic.detail import DetailView

from django.views.generic.list import ListView

from django.views.generic.edit import CreateView

from django.contrib.auth import get_user_model

from django.shortcuts import redirect

from .forms import UploadForm

from django.http import JsonResponse, HttpResponse


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

class UserListView(ListView):
    model = get_user_model()
    paginate_by = 10  
    template_name = "chat/user_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(pk=self.request.user.pk)
        return queryset

def create_chat(request, pk):
    chat = Chat.create_if_not_exists(request.user, pk)

    return redirect("room", pk=chat.pk)

def upload_file(request):
    chat = request.POST['chat_id']
    text = request.POST['text']
    message = ChatMessage.objects.create(sender=request.user, chat_id=chat, text=text)
    attachment = MessageAttachment.objects.create(file=request.FILES["file"], message=message)

    return JsonResponse({"url": attachment.file.url, "message_id": message.id})

def messages_history(request, pk):
    messages = ChatMessage.objects.filter(chat_id=pk)
    html = ""

    if messages.count() > 0:
        for message in messages:
            class_name = "bg-blue-500 text-white self-end p-2 rounded-lg"
            img = ""
            if message.sender.pk != request.user.pk:
                class_name = "bg-gray-300 text-black self-start p-2 rounded-lg"
            if message.file.exists():
                img = f'''
                    <img src="{message.file.first().file.url}" width="200" height="150">
                '''
            html += f'''
                <div id="m_{message.pk}" class="{class_name}">
                    {message.text}
                    {img}
                </div>
            '''

    return HttpResponse(html)

def unread_messages(request, pk):
    messages = ChatMessage.objects.exclude(read=True).exclude(sender=request.user)
    unread_messages = []

    for message in messages:
        image_url = None
        if message.file.exists():
            image_url = message.file.first().file.url

        unread_messages.append({"pk": message.id, "text": message.text, "url": image_url})    

    messages.update(read=True)
    return JsonResponse({"messages": unread_messages})
