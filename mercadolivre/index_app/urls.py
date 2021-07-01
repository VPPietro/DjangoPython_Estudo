from django.urls import path
from . import views
import index_app

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('index/', views.index_page, name='index_page'),
]
