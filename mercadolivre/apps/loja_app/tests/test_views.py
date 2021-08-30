from django.http import response
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from apps.user_app.models import UserModel
from apps.loja_app.models import ItensModel
from apps.loja_app.views import ItemCreateView, ItemUpdateView, ItemDeleteView
from apps.loja_app.forms import UpdateItemForm

def setup_std(self, factory=False, vendedor1=False, vendedor2=False, user=False, item=False):
    """Define valores padrões para as classes de teste"""
    self.factory = RequestFactory() if factory else None
    self.vendedor1 = UserModel.objects.create_superuser(
        email='supertest@gmail.com',
        username='superTest',
        password='123123123a',
        first_name= 'Super',
        last_name= 'Test',
        is_seller= True,
        ) if vendedor1 else None
    self.vendedor2 = UserModel.objects.create_superuser(
        email='supertest2@gmail.com',
        username='superTest2',
        password='123123123a',
        first_name= 'Super2',
        last_name= 'Test2',
        is_seller= True,
        ) if vendedor2 else None
    self.user = UserModel.objects.create_user(
                email='usertest@gmail.com',
                username='userTest',
                password='123123123a',
                first_name= 'User',
                last_name= 'Test',
                is_seller= False,
            ) if user else None
    self.item = ItensModel.objects.create(
        nome = 'Teste Item 1',
        descricao =  'Este é o item de teste 1',
        valor = 123456,
        quantidade = 2,
        vendedor = self.vendedor1,
        imagem = 'fotos/2021/07/30/scarlett.jpg'
        ) if item else None


class LojaCreateTest(TestCase):

    def setUp(self):
        setup_std(self, factory=True, vendedor1=True, user=True)
        self.request = self.factory.get('/loja/create/')
        self.redirect_code = list(range(300, 400))

    def test_redireciona_user_anonimo(self):
        """Teste para certificar que usuario anonimo não consegue acessar a página de criação de item,
        e se em seguida é redirecionado para tela de login"""
        self.request.user = AnonymousUser()
        response = ItemCreateView.as_view()(self.request)
        self.assertIn(response.status_code, self.redirect_code, 'Usuário anonimo não deve ter acesso a página de criação de item')
        self.assertIn('user/login', response.url, 'usuario não logado deve ser redirecionado para a tela de login')

    def test_redireciona_nao_vendedor(self):
        """Teste para se sertificar que usuario que não tem flag de vendedor acesse a página de criação de item,
        e em seguida é redirecionado para a tela de sua_loja"""
        self.request.user = self.user
        response = ItemCreateView.as_view()(self.request)
        self.assertIn(response.status_code, self.redirect_code, 'Usuário que não é vendedor também não deve ter acesso a página de criação de item')
        self.assertIn('sua_loja', response.url, 'usuario logado porem comprador, deve ser redirecionado para tela de sua_loja')

    def test_acesso_vendedor_pag_create(self):
        """Teste para se certificar que usuario logado com flag de vendedor tenha acesso a pagina de criação de item"""
        self.request.user = self.vendedor1
        response = ItemCreateView.as_view()(self.request)
        ok_code = list(range(200, 300))
        self.assertIn(response.status_code, ok_code, 'Usuário logado e vendedor, deve ter acesso a página de criação de item')


class LojaUpdateTest(TestCase):

    def setUp(self):
        setup_std(self, factory=True, vendedor1=True, item=True)

    def test_vendedor_atualiza_item(self):
        """Teste para se certificar se o vendedor criador do item consegue alterar as informações corretamente"""
        # Altera valores do item
        data = {'nome': 'Novo Item 2',
            'descricao': 'Este é o segundo item',
            'valor': 654321,
            'quantidade': 4,}
        self.request = self.factory.post('/loja/create/', data=data)
        self.request.user = self.vendedor1
        response = ItemUpdateView.as_view()(self.request, pk=self.item.id)
        form = UpdateItemForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 302)

        # Verifica novos valores do item
        self.item = ItensModel.objects.get(id=self.item.id)
        self.assertEqual(self.item.nome, 'Novo Item 2')
        self.assertEqual(self.item.descricao, 'Este é o segundo item')
        self.assertEqual(self.item.valor, 654321)
        self.assertEqual(self.item.vendedor, self.vendedor1)


class LojaDeleteTest(TestCase):

    def setUp(self):
        setup_std(self, factory=True, vendedor1=True, vendedor2=True, item=True)
        self.request = self.factory.post('/loja/delete')

    def test_nao_exclui_item_caso_nao_seja_dono_do_item(self):
        """Neste teste, o vendedor2 esta tentando excluir o item que pertence ao vendedor1, o vendedor2 não pode obter sucesso."""
        self.request.user = self.vendedor2
        # tenta excluir item
        ItemDeleteView.as_view()(self.request, pk=self.item.id)
        # verifica se o item ainda existe (deve existir)
        self.assertIn(self.item, ItensModel.objects.get_queryset(),
            'Item que não poderia ter sido excluido, foi excluido')

    def test_exclui_item_caso_seja_dono_do_item(self):
        """Neste caso o vendedor 1 esta tentando excluir o próprio item, o vendedor1 deve obter sucesso."""
        self.request.user = self.vendedor1
        # tenta excluir item
        ItemDeleteView.as_view()(self.request, pk=self.item.id)
        # verifica se item foi realmente excluido (nao deve existir)
        self.assertNotIn(self.item, ItensModel.objects.get_queryset(),
            'Item que deveria ter sido excluido, não foi excluido')
