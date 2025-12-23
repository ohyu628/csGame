from django.urls import path
from . import views

urlpatterns = [
    # 유저 개인 문제 관련 등록 및 조회
    path('problemsets/', views.problemset_create),
    path('problemsets/<int:set_pk>/', views.problemset_detail),
    path('problemsets/<int:set_pk>/problems/', views.problemset_problems),
    path('problem/<int:problem_pk>/', views.problem_detail),
]