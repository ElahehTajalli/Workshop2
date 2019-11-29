from django.urls import path
from . import views

urlpatterns = [
    path('conversation', views.conversation.as_view()),
    path('message', views.message_view.as_view())

]