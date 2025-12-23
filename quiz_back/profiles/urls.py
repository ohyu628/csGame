from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_profile),
    path("status/", views.my_profile_stats),
    path("status/<int:user_id>/", views.user_profile_stats),
    path("ranking/", views.ranking, name="ranking"),
]