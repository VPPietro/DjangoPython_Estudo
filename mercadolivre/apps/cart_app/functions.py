from apps.cart_app.models import CartModel


def get_or_create_cart(request):
    """Retorna o carrinho do user caso ele tenha ou cria um novo"""
    if request.user.is_authenticated:
        # caso o usuario já tenha carrinho, adiciona
        carrinho = CartModel.objects.filter(comprador=request.user.id)[0]
        if not carrinho:
            # caso o usuario não tenha carrinho, cria e adiciona
            carrinho = CartModel.objects.create(comprador=request.user)
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


def possui_carrinho(usuario):
    """Retorna True, caso o obj usuario tenha carrinho"""
    pass
