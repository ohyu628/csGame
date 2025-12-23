from django.urls import path
from . import views

urlpatterns = [
    # 인증 관련 CRD
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('me/', views.me, name='me'),
    path('delete/', views.delete, name='delete-account'), 

]