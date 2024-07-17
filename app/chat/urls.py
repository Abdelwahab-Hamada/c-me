from django.urls import path

from . import views

from .views import ChatDetailView, ChatListView, MessageAttachmentCreateView, upload_file

urlpatterns = [
    path("", ChatListView.as_view(), name="index"),
    path('upload/', upload_file, name='file-upload'),
    path("<slug:pk>/", ChatDetailView.as_view(), name="room"),
]