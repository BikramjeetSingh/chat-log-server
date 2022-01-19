from django.urls import path

from chats import views

urlpatterns = [
    path("chatlogs/<int:user_id>/", views.ChatLogListView.as_view(), name="chatlog-list"),
    path("chatlogs/<int:user_id>/<int:msg_id>", views.ChatLogDetailView.as_view(), name="chatlog-detail"),
]