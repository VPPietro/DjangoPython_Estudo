from django.urls import path
from . import views

urlpatterns = [
    path('sua_loja/', views.ItemListView.as_view(), name='lista-itens-user'),
    path('loja/create/', views.ItemCreateView.as_view(), name='criar-itens'),
    path('loja/<int:pk>/', views.ItemDetailView.as_view(), name='detalhe-item'),
    path('loja/<int:pk>/update', views.ItemUpdateView.as_view(), name='update-itens'),
    path('loja/<int:pk>/delete', views.ItemDeleteView.as_view(), name='deletar-itens'),
    path('', views.ItemListView.as_view(), name='index_page'),  # corrigir
]
