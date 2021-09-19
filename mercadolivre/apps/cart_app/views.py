from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http.response import HttpResponseBase

from apps.cart_app.views_functions import *

"""
Deletar carrinhos que não estão sendo usados mais
"""


class CartView(ListView):
    model = CartModel
    template_name = 'cart/cart.html'
    context_object_name = 'itens'

    def dispatch(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponseBase:
        """Chama join carts caso o user esteja logado e tenha cart anonimo"""
        self.carrinho, self.anonimo = ajusta_carrinho(request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: any): # adicionar total da compra
        cart_itens = None
        if self.request.user.is_authenticated and self.carrinho:
                cart_itens = get_cart_items(carrinho=self.carrinho)
        elif self.anonimo:
                cart_itens = get_cart_items(carrinho=self.anonimo)
        return {'itens': cart_itens}


class RemoveFromCart(DeleteView):
    model = CartItemModel
    success_url = reverse_lazy('cart_page')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def add_to_cart(request, **kwargs):
    pk = kwargs.get('pk', 0)
    carrinho, anonimo = get_or_create_cart(request)
    add_to_cart_func(pk, carrinho if carrinho else anonimo)
    return redirect(reverse_lazy('cart_page'))
