from apps.loja_app.models import ItensModel
from apps.cart_app.models import CartItemModel, CartModel


def get_or_create_cart(request):
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
        elif carrinho and carrinho_anonimo:
            # Se possui os dois carrinhos junta os itens dos dois
            carrinho_anonimo = CartModel.objects.select_related().get(id=carrinho_anonimo)
            join_carts(carrinho, carrinho_anonimo)
            # del request.session['carrinho']
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


def get_cart_items(request=None, carrinho=None):
    """Retorna Queryset de Cart Itens caso exista, ou []"""
    if request:
        carrinho = get_or_create_cart(request)
    cart_item = carrinho.cart_item.get_queryset()
    return cart_item

########## Corrigir, se o carrinho do user estiver vazio, não adiciona (se estiver vazio não era pra entrar no join_carts)
def join_carts(carrinho_user: CartModel, carrinho_anonimo: CartModel):
    carrinho_item_user = get_cart_items(carrinho=carrinho_user)
    carrinho_anonimo = get_cart_items(carrinho=carrinho_anonimo)
    print(carrinho_item_user)
    for u in carrinho_item_user:
        print('join cart for 1')
        for a in carrinho_anonimo:
            print('join cart for 2')
            if u.loja_item.id == a.loja_item.id:
                print('join cart entrou no if')
                # Caso o id dos itens sejam iguais,
                # soma a quantidade e deleta o item anonimo
                u.quantidade_compra += a.quantidade_compra
                u.save()
                a.delete()
            elif a.id:
                print('join cart entrou no elif')
                # Caso não exista o item no carrinho do user
                # e o item já não tenha sido deletado, adiciona no carrinho
                carrinho_user.cart_item.add(a)
            else:
                print('join cart entrou no else')


def add_to_cart_func(loja_item_id: int, carrinho: CartModel, quantidade=1):
    carrinho_itens = get_cart_items(carrinho=carrinho)
    # Verifica se o item existe no carrinho
    loja_ids = []
    for i in carrinho_itens:
        loja_ids.append(i.loja_item.id)
    try: item = loja_ids.index(loja_item_id)
    except ValueError: item = False

    # Caso exista:
    if item:
        carrinho_itens[item].quantidade_compra += quantidade
        carrinho_itens[item].save()
    else:
        item_loja = ItensModel.objects.filter(id=loja_item_id)
        if item_loja:
            item_loja = item_loja[0]
            item_cart = CartItemModel.objects.create(loja_item=item_loja, quantidade_compra=quantidade)
            carrinho.cart_item.add(item_cart)




    # for i in carrinho_itens:
    #     if loja_item_id == i.loja_item.id:
    #         i.quantidade_compra += quantidade
    #         i.save()
    #         break
    #     else:
    #         item_loja = ItensModel.objects.filter(id=loja_item_id)
    #         if item_loja:
    #             item_loja = item_loja[0]
    #             item_cart = CartItemModel.objects.create(loja_item=item_loja, quantidade_compra=quantidade)
    #             carrinho.cart_item.add(item_cart)
    #         break