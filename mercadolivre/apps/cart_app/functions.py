from django.http import response
from django.http.request import HttpRequest
from apps.loja_app.models import ItensModel
from apps.cart_app.models import CartItemModel, CartModel


def get_or_create_cart_old(request):
    """Retorna o carrinho do user caso ele tenha ou cria um novo"""
    if request.user.is_authenticated:
        carrinho = CartModel.objects.filter(comprador=request.user.id)
        carrinho = carrinho[0] if carrinho else None
        carrinho_anonimo = request.session.get('carrinho', False)
        if not carrinho:
            # caso user nao tenha carrinho
            if carrinho_anonimo:
                # Caso tenha carrinho_anonimo vincula carrinho_anonimo para o usuario
                print('carrinho_anonimo', carrinho_anonimo, '\n', 'carrinho', carrinho)
                carrinho = CartModel.objects.select_related().get(id=carrinho_anonimo)
                carrinho.comprador = request.user
                carrinho.save()
            else:
                # caso o usuario não tenha carrinho anonimo nem do user, cria um novo
                carrinho = CartModel.objects.create(comprador=request.user)
                print('criou novo')
        elif carrinho and carrinho_anonimo:
            # Se possui os dois carrinhos junta os itens dos dois
            carrinho_anonimo = CartModel.objects.select_related().get(id=carrinho_anonimo)
            join_carts(carrinho, carrinho_anonimo)
            # del request.session['carrinho']
        else:
            # Se possui os dois carrinhos, mas não possui nenhum item no carrinho atual
            pass
    else:
        # Caso o user seja anonimo verifica se possui carrinho
        carrinho = CartModel.objects.filter(id=request.session.get('carrinho'))
        if not carrinho:
            # Caso não tenha carrinho, cria um novo e atribui à session
            carrinho = CartModel.objects.create()
            request.session['carrinho'] = carrinho.id
        else:
            carrinho = carrinho[0]
    return carrinho


def get_cart_data(request: HttpRequest):
    carrinho, anonimo = get_or_create_cart(request)
    request.session['carrinho_user'] = carrinho.id
    request.session['carrinho_anonimo'] = anonimo.id if isinstance(anonimo, CartModel) else None
    print(request.session.get('carrinho_user'), request.session.get('carrinho_anonimo'))

def get_or_create_cart(request):
    """Retorna o carrinho do user caso ele tenha ou cria um novo"""
    print('get_or_create_cart')
    anonimo = request.session.get('carrinho', False)
    if request.user.is_authenticated:
        # Seleciona ou cria um carrinho pro user logado
        carrinho = CartModel.objects.filter(comprador=request.user.id)
        carrinho = carrinho[0] if carrinho else cria_carrinho(request.user)
        if anonimo:
            try: anonimo = CartModel.objects.get(id=anonimo)
            except ValueError: anonimo = False
    else:
        # Seleciona ou cria um carrinho pro user anonimo
        carrinho = CartModel.objects.filter(id=anonimo)
        carrinho = carrinho[0] if carrinho else cria_carrinho()
        request.session['carrinho'] = carrinho.id
    return carrinho, anonimo


def cria_carrinho(user=None):
    print('cria_carrinho')
    return CartModel.objects.create(comprador=user)


def tranfere_itens_de_carrinho(origem: CartModel, destino: CartModel):
    pass


def get_cart_items(request=None, carrinho=None):
    print('get_cart_items')
    """Retorna Queryset de Cart Itens caso exista, ou []"""
    if request:
        carrinho = get_or_create_cart(request)[0]
    cart_item = carrinho.cart_item.get_queryset()
    return cart_item

# nao junta todos os itens
def join_carts(carrinho_user: CartModel, carrinho_anonimo: CartModel):
    print('join_carts')
    carrinho_item_user = carrinho_user.cart_item.get_queryset()
    carrinho_anonimo = carrinho_anonimo.cart_item.get_queryset()
    for u in carrinho_item_user:
        for a in carrinho_anonimo:
            if u.loja_item.id == a.loja_item.id:
                # Caso tenha o item no carrinho
                u.quantidade_compra += a.quantidade_compra
                u.save()
                a.delete()
            elif a.id:
                # Caso não exista o item no carrinho
                carrinho_user.cart_item.add(a)
        carrinho_anonimo.delete()


def add_to_cart_func(loja_item_id: int, carrinho: CartModel, quantidade=1):
    print('add_to_cart_func')
    carrinho_itens = get_cart_items(carrinho=carrinho)
    # Verifica se o item existe no carrinho
    loja_ids = []
    for i in carrinho_itens:
        loja_ids.append(i.loja_item.id)
    try: item = loja_ids.index(loja_item_id)
    except ValueError: item = False
    if item:
        carrinho_itens[item].quantidade_compra += quantidade
        carrinho_itens[item].save()
    else:
        item_loja = ItensModel.objects.filter(id=loja_item_id)
        if item_loja:
            item_loja = item_loja[0]
            item_cart = CartItemModel.objects.create(loja_item=item_loja, quantidade_compra=quantidade)
            carrinho.cart_item.add(item_cart)
