from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from apps.loja_app.models import ItensModel
from apps.cart_app.models import CartItemModel, CartModel


def get_or_create_cart(request: HttpRequest) -> tuple:
    """Retorna tupla de carrinho ou false para carrinho do user e anonimo"""
    carrinho = False
    anonimo = request.session.get('anonimo', False)
    if request.user.is_authenticated:
        # Seleciona ou cria um carrinho pro user logado
        carrinho = CartModel.objects.select_related().filter(comprador=request.user.id)
        carrinho = carrinho[0] if carrinho else cria_carrinho(request.user)
        if anonimo:
            try: anonimo = CartModel.objects.select_related().get(id=anonimo)
            except: anonimo = False
    else:
        # Seleciona ou cria um carrinho pro user anonimo
        anonimo = CartModel.objects.select_related().filter(id=anonimo)
        anonimo = anonimo[0] if anonimo else cria_carrinho()
        request.session['anonimo'] = anonimo.id
    return carrinho, anonimo


def get_cart_items(carrinho: CartModel) -> QuerySet:
    """Retorna Queryset de Cart Itens caso exista, ou []"""
    # Caso não precise de select no banco (carrinho está com select_related):
    try: cart_item = carrinho.cart_item.all()
    # Caso precise, faz o select
    except: cart_item = carrinho.cart_item.get_queryset()
    return cart_item


def ajusta_carrinho(request: HttpRequest) -> tuple:
    """Junta ou inclui itens de carrinhos"""
    carrinho, anonimo = get_or_create_cart(request)
    if carrinho and anonimo:
        join_carts(carrinho, anonimo)
        deleta_carrinho(anonimo)
        del request.session['anonimo']
    return carrinho, anonimo


def cria_carrinho(user=None) -> CartModel:
    """Cria um carrinho para o user informado, caso não seja informado nenhum
    será retornado um Cart sem user."""
    return CartModel.objects.create(comprador=user)


def deleta_carrinho(carrinho: CartModel):
    if isinstance(carrinho, CartModel):
        carrinho.delete()


def join_carts(carrinho: CartModel, anonimo: CartModel):
    carrinho_itens = get_cart_items(carrinho)
    anonimo_itens = get_cart_items(anonimo)
    if carrinho_itens and anonimo_itens:
        for u in carrinho_itens:
            for a in anonimo_itens:
                if u.loja_item == a.loja_item:
                    u.quantidade_compra += a.quantidade_compra
                    u.save()
                    a.delete()
                elif a.id:
                    carrinho.cart_item.add(a)
    elif anonimo_itens:
        for a in anonimo_itens:
            carrinho.cart_item.add(a)
            carrinho.save()


def add_to_cart_func(loja_item_id: int, carrinho: CartModel, quantidade=1):
    """Cria ou adiciona item no carrinho indicado"""
    carrinho_itens = list(get_cart_items(carrinho=carrinho))
    # Verifica se o item existe no carrinho
    for item in carrinho_itens:
        if loja_item_id == item.loja_item.id:
            index = carrinho_itens.index(item)
            carrinho_itens[index].quantidade_compra += quantidade
            carrinho_itens[index].save()
            return
    item_loja = ItensModel.objects.filter(id=loja_item_id)
    if item_loja:
        item_loja = item_loja[0]
        item_cart = CartItemModel.objects.create(
            loja_item=item_loja, quantidade_compra=quantidade)
        carrinho.cart_item.add(item_cart)
