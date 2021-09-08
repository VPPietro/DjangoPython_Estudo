from django.urls import path

from apps.cart_app import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart_page'),
    # path('add)
]