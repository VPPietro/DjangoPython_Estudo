from django.urls import path

from apps.cart_app import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart_page'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>', views.RemoveFromCart.as_view(), name='remove_from_cart'),
]
