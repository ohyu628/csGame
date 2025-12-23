from django.urls import path
from game import views

urlpatterns = [
    # 게임모드 관련 문제 조회 url
    # 조회
    # 메인 모드
    path('maps/', views.map_list),  # 맵 목록 조회
    path('maps/<int:map_pk>/', views.map_detail),   # 맵 리스트안 문제집 정보 조회
    path('quiz/play/', views.start_play_session),  # 문제집 플레이
    # 채점
    path('quiz/check/', views.check_answer),
    # 자유 모드
    path('users/<int:user_pk>/problemsets/', views.user_problem_set),   # 특정 유저 문제집
    path('users/problemsets/', views.user_created_problem_set),   # 유저 문제집 목록 조회
    # ai
    path('history/', views.recent_wrong_logs),
]