from django.urls import path
from chat.views import message_view,message_to_user,MessageDeleteView
app_name="chat"
urlpatterns=[
    path("messages/",message_view,name="messages"),
    path("messages/<str:username>/",message_to_user,name="messages_user"),
    path("messages/delete/<int:pk>/",MessageDeleteView.as_view(template_name="message_confirm_delete.html"),name="message_delete")
]