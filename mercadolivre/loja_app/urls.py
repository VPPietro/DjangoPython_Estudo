from django.urls import path
from . import views

urlpatterns = [
    path('', views.ItemListView.as_view(), name='lista-itens'),
    path('create/', views.ItemCreateView.as_view(), name='criar-itens'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='detalhe-itens'),
    path('<int:pk>/update', views.ItemUpdateView.as_view(), name='update-itens'),
    path('<int:pk>/delete', views.ItemDeleteView.as_view(), name='deletar-itens'),
]
