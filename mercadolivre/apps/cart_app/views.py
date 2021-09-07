from apps.loja_app.models import ItensModel
from django.views.generic import ListView

from apps.cart_app.models import CartModel


class CartView(ListView):
    model = CartModel
    template_name = 'cart/cart.html'
    context_object_name = 'itens'
