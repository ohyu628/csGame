from django.urls import path
from . import views

urlpatterns = [
    path("echo/", views.ai_echo),
    path("feedback/", views.wrong_feedback),
]