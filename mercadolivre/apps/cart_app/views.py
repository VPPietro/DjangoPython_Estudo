from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpRequest
from django.http.response import HttpResponseBase

from apps.cart_app.functions import *
from apps.cart_app.models import  CartItemModel, CartItemModel

"""
Vincular com a tela de login, mesclar cart de user anonimo com cart do user que fez login
"""


class CartView(ListView):
    model = CartModel
    template_name = 'cart/cart.html'
    context_object_name = 'itens'

    def dispatch(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponseBase:
        ##### Verificar se o user esta autenticado
        if request.user.is_authenticated:
            ####  Verificar se o user tem cart anonimo
            if request.session.get('carrinho', False):
                ###   Chamar a função de join carts
                self.carrinho, anonimo = get_or_create_cart(request)
                join_carts(self.carrinho, anonimo)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: any): # adicionar total da compra
        if not self.carrinho:
            cart_itens = get_cart_items(self.request)
        else:
            cart_itens = get_cart_items(carrinho=self.carrinho)
        return {'itens': cart_itens}


class RemoveFromCart(DeleteView):
    model = CartItemModel
    success_url = reverse_lazy('cart_page')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def add_to_cart(request, **kwargs):
    """Falta:   - verificar se quantidade a adicionar no carrinho é maior que a quantidade em estoque do produto
                - verificar se tem dois cart_item com loja_items iguais e unificar
        Tests   - Se um usuário não tem um carrinho, deve criar automáticamente
                - """
    pk = kwargs.get('pk', 0)
    carrinho, id_carrinho_anono = get_or_create_cart(request)
    add_to_cart_func(pk, carrinho)
    return redirect(reverse_lazy('cart_page'))
