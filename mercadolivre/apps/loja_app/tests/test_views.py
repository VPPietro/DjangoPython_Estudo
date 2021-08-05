from apps.loja_app.models import ItensModel
from apps.user_app.models import UserModel
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.contrib.messages.storage.fallback import FallbackStorage

from apps.loja_app.views import ItemCreateView, ItemListView


class LojaViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = UserModel.objects.create_superuser(
            email='supertest@gmail.com',
            username='superTest',
            password='123123123a',
            first_name= 'Super',
            last_name= 'Test',
            is_seller= True,
        )
        self.user = UserModel.objects.create_user(
            email='usertest@gmail.com',
            username='userTest',
            password='123123123a',
            first_name= 'User',
            last_name= 'Test',
            is_seller= False,
        )
        self.request = self.factory.get('/loja/create/')
        self.redirect_code = list(range(300, 400))

    def test_redireciona_user_anonimo(self):
        self.request.user = AnonymousUser()
        response = ItemCreateView.as_view()(self.request)
        self.assertIn(response.status_code, self.redirect_code, 'Usuário anonimo não deve ter acesso a página de criação de item')

    def test_redireciona_nao_vendedor(self):
        self.request.user = self.user
        response = ItemCreateView.as_view()(self.request)
        self.assertIn(response.status_code, self.redirect_code, 'Usuário que não é vendedor também não deve ter acesso a página de criação de item')

    def test_acesso_vendedor_pag_create(self):
        self.request.user = self.superuser
        response = ItemCreateView.as_view()(self.request)
        ok_code = list(range(200, 300))
        self.assertIn(response.status_code, ok_code, 'Usuário logado e vendedor, deve ter acesso a página de criação de item')

    def test_cria_item(self):
        item = ItensModel(
            nome = 'Teste Item 1',
            descricao =  'Este é o item de teste 1',
            valor = 123456,
            quantidade = 2,
            vendedor = self.superuser,
            imagem = 'fotos/2021/07/30/scarlett.jpg'
        )
        self.assertEqual(item.nome, 'Teste Item 1')
        self.assertEqual(item.descricao, 'Este é o item de teste 1')
        self.assertEqual(item.valor, 123456)
        self.assertEqual(item.quantidade, 2)
        self.assertEqual(item.vendedor, self.superuser)
        self.assertEqual(item.imagem, 'fotos/2021/07/30/scarlett.jpg')

        # data = {
        #     'nome': 'Teste Item 1',
        #     'descricao': 'Este é o item de teste 1',
        #     'valor': 123456,
        #     'quantidade': 2,
        #     'vendedor': self.superuser,
        #     'imagem': 'fotos/2021/07/30/scarlett.jpg'
        # }
        # self.request = self.factory.post('/loja/create', data)
        # self.request.user = self.superuser
        # setattr(self.request, 'session', 'session')
        # setattr(self.request, '_messages', FallbackStorage(self.request))
        # response = ItemCreateView.as_view()(self.request)
        # self.assertEquals(response.status_code, 200) 

        # MOVER PARA TEST DE LOGIN
        # browser = webdriver.Chrome(ChromeDriverManager().install())
        # # Obter a página de Login
        # browser.get('http://127.0.0.1:8000/user/login')
        # # Obter itens da página de login
        # email = browser.find_element_by_id('emailinput')
        # senha = browser.find_element_by_id('passwordinput')
        # entrar = browser.find_element_by_id('submitbtn')

        # # Enviar informações para campos
        # email.send_keys('supertest@gmail.com')
        # senha.send_keys('123123123a')
        # entrar.send_keys(Keys.RETURN)
