from datetime import timezone
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_page'),
    path('signin/', views.signin_view, name='signin_page'),
    path('logoff/', views.logoff_view, name='logoff_page'),
    path('info/', views.user_info_view, name='user_info_page'),
    path('alterinfo/', views.alter_user_info_view, name='alter_user_info_page')
]
