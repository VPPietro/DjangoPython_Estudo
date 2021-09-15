from apps.cart_app.models import CartModel


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


def join_carts_old(carrinho_user: CartModel, carrinho_anonimo: CartModel):
    """Junta o carrinho do usuário anonimo com do usuário que fizer login"""
    list_cart_anonimo_items = list(get_cart_items(carrinho=carrinho_anonimo))
    list_cart_user_items = list(get_cart_items(carrinho=carrinho_user))
    list_user_items_id = []
    for y in list_cart_user_items:
        list_user_items_id.append(y.loja_item.id)
    for i in list_cart_anonimo_items:
        if i.loja_item.id in list_user_items_id:
            item_user = list_cart_user_items[list_user_items_id.index(i.loja_item.id)]
            quantidade_total = i.quantidade_compra + item_user.quantidade_compra
            item = carrinho_user.cart_item.get(id=item_user.id)
            item.quantidade_compra = quantidade_total
            item.save()
        else:
            carrinho_user.cart_item.add(i)


def join_carts(carrinho_user: CartModel, carrinho_anonimo: CartModel):
    itens_cart_anonimo = list(get_cart_items(carrinho=carrinho_anonimo))
    itens_cart_user = list(get_cart_items(carrinho=carrinho_user))
    itens_repetidos = set(itens_cart_user).intersection(itens_cart_anonimo)
    print(itens_cart_user, itens_cart_anonimo)
    for i in itens_cart_anonimo:
        try: item = itens_cart_user[itens_cart_user.index(i)]
        except: item = None
        print(item)
        if item:
            if i == item:
                print('dentro do itens cart user')
                print(itens_cart_anonimo, itens_cart_user)
                item = itens_cart_user[itens_cart_user.index(i)]
                item.quantidade_compra += i.quantidade_compra
                item.save()
        else:
            carrinho_user.cart_item.add(i)




    # itens_repetidos = set(itens_cart_user).intersection(itens_cart_anonimo)
    # print(itens_repetidos)


