from django.shortcuts import render

from django.utils import timezone

from chat.models import ChatMessage, Chat, MessageAttachment

from django.views.generic.detail import DetailView

from django.views.generic.list import ListView

from django.views.generic.edit import CreateView

from .forms import UploadForm

from django.http import JsonResponse

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

class MessageAttachmentCreateView(CreateView):
    model = MessageAttachment
    form_class = UploadForm

    def form_valid(self, form: UploadForm):
        chat = form.cleaned_data['chat_id']
        text = form.cleaned_data['text']
        message = ChatMessage.objects.create(sender=self.request.user, chat_id=chat, text=text)
        self.object = MessageAttachment.objects.create(file=form.cleaned_data['file'], message=message)
        return JsonResponse({"a7a":55555555555})

def upload_file(request):
    chat = request.POST['chat_id']
    text = request.POST['text']
    message = ChatMessage.objects.create(sender=request.user, chat_id=chat, text=text)
    attachment = MessageAttachment.objects.create(file=request.FILES["file"], message=message)

    return JsonResponse({"url": attachment.file.url, "message_id": message.id})
