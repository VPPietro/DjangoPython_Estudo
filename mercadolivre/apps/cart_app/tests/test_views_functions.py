from django.test import TestCase


class get_or_create_cartTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_request_com_somente_cart_anonimo(self):
        """Verifica se a função retorna False e obj cart_anonimo"""
        # define uma request somente com cart anonimo
        # manda para a função
        # verifica se retorna False, obj cart_anonimo
        pass

    def t_request_com_somente_cart_user(self):
        """Verifica se a função retorna obj cart_user e False"""
        # define uma request somente com cart user
        # manda para a função
        # verifica se retorna obj cart_user e False
        pass

    def t_request_com_os_dois_carts(self):
        """Verifica se a função retorna obj cart_user e obj cart_anonimo"""
        # define uma request com os dois carts
        # manda para a função
        # verifica se retorna obj cart_user e obj cart_anonimo
        pass


class get_cart_itemsTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_manda_carrinho_com_itens(self):
        """Verifica se ao mandar carrinho com itens, é retornado um queryset
        com cart_items"""
        # cria um carrinho com itens
        # manda o carrinho para a função
        # verifica se retornou queryset com os cart_items
        pass

    def t_manda_carrinho_sem_itens(self):
        """Verifica se ao mandar carrinho sem itens, é retornado um queryset vazio"""
        # cria um carrinho sem itens
        # manda o carrinho para a função
        # verifica se retornou queryset vazio
        pass


class ajusta_carrinhoTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_user_anonimo_com_carrinho(self):
        """Verifica se a função retorna o carrinho do user anonimo sem alterações"""
        # define uma request com user anonimo e carrinho
        # manda para a função
        # verifica se retorna False para cart anonimo
        pass

    def t_user_anonimo_sem_carrinho(self):
        """Verifica se a função retorna um novo carrinho para o user anonimo"""
        # define uma request com user anonimo e sem carrinho
        # manda para a função
        # verifica se retorna um novo carrinho para o user anonimo
        pass

    def t_user_logado_sem_carrinho_anonimo(self):
        """Verifica se a função retorna o carrinho do user sem alterações"""
        # define uma request com user logado, sem carrinho anonimo
        # manda para a função
        # verifica se retorna o cart do user sem alterações
        pass

    def t_user_logado_com_carrinho_anonimo(self):
        """Verifica se a função retorna o carrinho do user junto com os itens do carrinho anonimo"""
        # define uma request com user logado, com carrinho anonimo
        # manda para a função
        # verifica se retorna o cart do user junto com os itens do carrinho anonimo
        pass



class cria_carrinhoTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_cria_carrinho_anonimo(self):
        """Cria um carrinho sem um user, ou seja, anonimo"""
        # chama a função sem nenhum valor informado
        # verifica se é retornado um CartModel sem usuário
        pass

    def t_cria_carrinho_com_user(self):
        """Cria um carrinho com um user"""
        # chama a função informando um user
        # verifica se é retornado um CartModel com o usuário informado
        pass


class deleta_carrinhoTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_deleta_carrinho(self):
        """Verifica se a função deleta um carrinho"""
        # manda um carrinho para a função
        # verifica se o carrinho foi deletado
        pass


class join_cartsTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_manda_carrinho_vazio_anonimo_com_item(self):
        """Verifica se será adicionado os itens do cart anonimo para o cart do user"""
        # manda um carrinho vazio e um carrinho anonimo com item para a função
        # verifica se o carrinho anonimo ficou vazio (talvez precise definir a.delete() nos elifs (linhas 66 e 68))
        # verifica se o carrinho user esta com os itens
        pass

    def t_manda_carrinho_com_item_anonimo_vazio(self):
        """A função não deve fazer nada, pois não é necessário alterar"""
        # manda um carrinho com itens e um carrinho anonimo vazio para a função
        # verifica se nenhuma alteração foi feita
        pass

    def t_manda_todos_carrinhos_com_itens(self):
        """Verifica se será adicionado os itens do cart anonimo para o cart do user"""
        # manda um carrinho com um iten x e um carrinho anonimo com iten x e y para a função
        # verifica se o carrinho anonimo ficou vazio (talvez precise definir a.delete() nos elifs (linhas 66 e 68))
        # verifica se o carrinho user esta com os itens x + 1 e y
        pass


class add_to_cart_funcTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_manda_item_existente_no_carrinho(self):
        """Verifica se ao mandar um item que já existe no carrinho
        o mesmo não será duplicado, mas sim, terá sua quantidade aumentada"""
        # manda um id de um item que já esta no carrinho
        # verifica se a quantidade do item aumentou
        # verifica se o item não foi duplicado
        pass

    def t_manda_item_inexistente_no_carrinho(self):
        """Verifica se ao mandar um item que não existe no carrinho, é criado um novo"""
        # manda um id de um item que não está no carrinho
        # verifica se o item foi adicionado
        # verifica se o item não foi duplicado
        pass
