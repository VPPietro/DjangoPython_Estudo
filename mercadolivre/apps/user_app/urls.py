from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginClassView.as_view(), name='login_page'),
    path('signup/', views.SignUpClassView.as_view(), name='signup_page'),
    path('logoff/', views.LogoutView.as_view(), name='logoff_page'),
    path('', views.InfoUserClassView.as_view(), name='user_info_page'),
    path('update/', views.UpdateUserInfoClassView.as_view(), name='alter_user_info_page'),
]
