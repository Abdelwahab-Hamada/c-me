from django.urls import path

from . import views

from chat.views import ChatDetailView

from chat.views import ChatListView


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]

urlpatterns = [
    path("<slug:slug>/", ChatDetailView.as_view(), name="chat-detail"),
]

urlpatterns = [
    path("", ChatListView.as_view(), name="chat-list"),
]