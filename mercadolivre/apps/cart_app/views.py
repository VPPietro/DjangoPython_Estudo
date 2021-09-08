from django.views.generic import ListView

from apps.loja_app.models import ItensModel
from apps.cart_app.models import CartItemModel, CartModel


class CartView(ListView):
    model = CartModel
    template_name = 'cart/cart.html'
    context_object_name = 'itens'

    def get_context_data(self, **kwargs: any):
        cart = CartModel.objects.get_queryset().filter(comprador_id=self.request.user.id)
        if cart:
            print(dir(cart[0]))
            print(cart[0].comprador)
            print(cart[0].cart_item)
            print(cart[0].id)
        return {'itens': cart}
