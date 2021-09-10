from django.views.generic import ListView, View, CreateView
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from apps.loja_app.models import ItensModel
from apps.cart_app.models import  CartModel, CartItemModel


# class CartView(ListView):
#     model = CartModel
#     template_name = 'cart/cart.html'
#     context_object_name = 'itens'

#     def dispatch(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponseBase:
#         # Verifica se o usuário já tem um carrinho
#             # Caso não tenha, redireciona para a página de criação de carrinho
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs: any):
#         context = super().get_context_data(**kwargs)
#         print(context.get('object_list'))
#         return context


def cart_view(request, **kwargs):
    """Falta:   - criar carrinhos para logados e nao logados
                - verificar se tem dois cart_item com loja_items iguais e unificar
                - corrigir, para caso acesse a página de cart e não tenha nenhum item (atualmente quebra a página)"""
    cart = CartModel.objects.filter(comprador_id=request.user.id)[0]
    cart_itens = CartItemModel.objects.get_queryset().filter(cartmodel=cart.id)
    print(cart, cart_itens)
    return render(request, 'cart/cart.html', {'itens': cart_itens})

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
        # Caso o item exista, cria um cart item e seleciona um carrinho caso exista
        cart_item = CartItemModel.objects.create(loja_item=item[0], quantidade_compra=quantidade)
        carrinho = CartModel.objects.filter(comprador=request.user.id)
        if carrinho:
            # caso o usuario já tenha carrinho, adiciona
            carrinho[0].cart_item.add(cart_item)
        else:
            # caso o usuario não tenha carrinho, cria e adiciona
            carrinho = CartModel.objects.create(comprador=request.user)
            carrinho.cart_item.add(cart_item)
    return redirect(reverse_lazy('cart_page'))
