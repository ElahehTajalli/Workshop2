
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('user', views.user_view.as_view()),
    path('login', csrf_exempt(views.login_view.as_view()))
]
