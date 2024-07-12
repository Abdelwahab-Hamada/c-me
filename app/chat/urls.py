from django.urls import path

from . import views

from .views import ChatDetailView

from .views import ChatListView


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]

urlpatterns = [
    path("details", ChatDetailView.as_view(), name="chat-detail"),
]

urlpatterns = [
    path("list", ChatListView.as_view(), name="chat-list"),
]