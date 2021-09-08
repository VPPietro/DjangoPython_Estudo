from django.views.generic import ListView

from apps.loja_app.models import ItensModel
from apps.cart_app.models import CartItemModel, CartModel


class CartView(ListView):
    model = CartModel
    template_name = 'cart/cart.html'
    context_object_name = 'itens'

    def get_queryset(self):
        if self.request.user.is_anonymous:
            CartItemModel
        return super().get_queryset()
