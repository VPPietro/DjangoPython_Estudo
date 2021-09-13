from apps.cart_app.models import CartModel


def get_or_create_cart(request):
    """Retorna o carrinho do user caso ele tenha ou cria um novo"""
    if request.user.is_authenticated:
        # caso o usuario já tenha carrinho, adiciona
        carrinho = CartModel.objects.filter(comprador=request.user.id)[0]
        carrinho_anonimo = request.session.get('carrinho', False)
        if not carrinho:
            if carrinho_anonimo:
                # Caso tenha carrinho anonimo vincula carrinho para o usuario
                pass
            # caso o usuario não tenha carrinho anonimo nem do user, cria e adiciona
            carrinho = CartModel.objects.create(comprador=request.user)
        elif carrinho and carrinho_anonimo:
            # Se possui os dois carrinhos junta os itens dos dois
            pass

    else:
        # Caso o user seja anonimo verifica se possui carrinho
        carrinho = CartModel.objects.filter(id=request.session.get('carrinho'))
        if not carrinho:
            # Caso não tenha carrinho, cria um novo
            request.session['carrinho'] = CartModel.objects.create().id
            carrinho = CartModel.objects.filter(id=request.session.get('carrinho'))[0]
        else:
            carrinho = carrinho[0]
    return carrinho


def get_cart_items(request):
    """Retorna Queryset de Cart Itens caso exista, ou []"""
    carrinho = get_or_create_cart(request)
    cart_item = carrinho.cart_item.get_queryset()
    return cart_item


def join_carts(carrinho_user, carrinho_anonimo):
    """Junta o carrinho do usuário anonimo com do usuário que fizer login"""
    print(f'carrinho anonimo: {carrinho_anonimo}\n', f'carrinho request: {carrinho_user}')
    pass


def possui_carrinho(usuario):
    """Retorna True, caso o obj usuario tenha carrinho"""
    pass
