from django.views.generic import ListView, View, CreateView
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.shortcuts import render

from apps.loja_app.models import ItensModel
from apps.cart_app.models import  CartModel


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
    cart = CartModel.objects.filter(comprador_id=request.user.id)[0]
    # cart_itens = CartItemModel.objects.get_queryset().filter(cartmodel=cart.id)
    # for item in cart_itens:
    #     print(item)
        # print(dir(item.item))
    # print(cart, dir(cart_itens))
    return render(request, 'cart/cart.html', {'itens': cart})

def add_to_cart(request, **kwargs):
    item = ItensModel.objects.filter(id=kwargs.get('pk', 0))
    quantidade = 1
    # create = CartItemModel.objects.create(item=item[0], quantidade=1)
    print(kwargs.get('pk', 0))
    return render(request, 'cart/add_to_cart.html')