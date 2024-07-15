from django.urls import path

from . import views

from .views import ChatDetailView
from .views import ChatListView

urlpatterns = [
    path("", ChatListView.as_view(), name="index"),
    path("<slug:pk>/", ChatDetailView.as_view(), name="room"),
]