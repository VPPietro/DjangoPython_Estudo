from loja_app import views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.items_list_view, name='list-itens'),
    path('create/', views.items_create_view, name='create-itens'),
]
