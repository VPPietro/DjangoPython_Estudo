from django.views.generic import ListView, CreateView
from django.views.generic.edit import DeleteView
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.cart_app.functions import *
from apps.loja_app.models import ItensModel
from apps.cart_app.models import  CartItemModel, CartItemModel

"""
Vincular com a tela de login, mesclar cart de user anonimo com cart do user que fez login
"""


class CartView(ListView):
    model = CartModel
    template_name = 'cart/cart.html'
    context_object_name = 'itens'

    def get_context_data(self, **kwargs: any): # adicionar total da compra
        cart_itens = get_cart_items(self.request)
        return {'itens': cart_itens}


def add_to_cart(request, **kwargs):
    """Falta:   - verificar se quantidade a adicionar no carrinho é maior que a quantidade em estoque do produto
                - verificar se tem dois cart_item com loja_items iguais e unificar
        Tests   - Se um usuário não tem um carrinho, deve criar automáticamente
                - """
    pk = kwargs.get('pk', 0)
    item = None
    if pk:
        # Caso tenha id do item no link, faz select do item
        item = ItensModel.objects.filter(id=pk)
        quantidade = 1
    if item:
        # Caso o item exista, testa se existe o item no carrinho
        # Caso tenha o item no carrinho incremente a quantidade
        # Caso não tenha o item no carrinho, cria um cart_item e adiciona no carrinho
        cart_item = CartItemModel.objects.create(loja_item=item[0], quantidade_compra=quantidade)
        carrinho = get_or_create_cart(request)
        carrinho.cart_item.add(cart_item)
    return redirect(reverse_lazy('cart_page'))


class RemoveFromCart(DeleteView):
    model = CartItemModel
    success_url = reverse_lazy('cart_page')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
