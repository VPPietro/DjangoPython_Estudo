from os import setuid
from django.http import response
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls.base import reverse_lazy

from apps.user_app.models import UserModel
from apps.user_app.views import LoginClassView, SignUpClassView


def setup_std(self, factory=True, user=False, user2=False):
    self.factory = RequestFactory() if factory else None
    self.user = UserModel.objects.create_user(
        email='usertest@gmail.com',
        username='userTest',
        password='123123123a',
        first_name='User',
        last_name='Test',
        is_seller=False,) if user else None
    self.user2 = UserModel.objects.create_user(
        email='usertest2@gmail.com',
        username='userTest2',
        password='123123123a',
        first_name='User',
        last_name='Test',
        is_seller=False,) if user2 else None


def user_existente(self, nome_do_user: str) -> bool:
    """Busca no queryset se o usuário passado existe, retorna True caso positivo"""
    user = UserModel.objects.get_queryset().filter(username=nome_do_user)
    return False if len(user) < 1 else True


def mesma_pagina(response, pagina: str) -> bool:
    return response.wsgi_request.path == pagina


class LoginViewTest(TestCase):

    def setUp(self):
        setup_std(self, user=True, user2=True)

    def test_login_com_usuario_incorreto(self):
        """Testa se quando enviado uma requisição com informações incorretas de login,
        se manterá um usuário anonymo, e se manterá na página de login"""
        # manda uma request tipo post com informações de usuario incorretas
        data = {
            'username': 'usertest@gmail.com',
            'password': '123123123aerrado'}
        response = self.client.post('/user/login/', data, follow=True)
        # Verifica se a página se manteve em '/user/login/'
        self.assertEqual(response.request['PATH_INFO'], '/user/login/')
        # Verifica se a request continua com o user AnonymousUser()
        self.assertTrue(isinstance(response.context['user'], AnonymousUser))

    def test_login_com_usuario_correto(self):
        """Testa se quando enviado uma requisição com informações corretas de login,
        o usuário é logado corretamente e redirecionado para a página 'sua loja'"""
        # manda uma request tipo post com informações de usuario corretas
        data = {
            'username': 'usertest@gmail.com',
            'password': '123123123a'}
        response = self.client.post('/user/login/', data, follow=True)
        # Verifica se a página foi redirecionada para 'lista-itens-user'
        self.assertEqual(response.request['PATH_INFO'], '/sua_loja/')
        # Verifica se a request esta com o user logado
        self.assertEqual(response.context['user'], self.user)

    def test_acesso_a_pagina_login_com_usuario_ja_logado(self):
        """Testa se um usuario tentar entrar na página de login já estando logado
        será redirecionado para a página de 'sua loja' e se mantém o mesmo usuário logado"""
        # tenta mandar uma request do tipo get para a página de login
        self.request = self.factory.get('/user/login')
        self.request.user = self.user
        response = LoginClassView.as_view()(self.request)
        # Verifica se o usuario foi redirecionado para a pagina de 'lista-itens-user'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/sua_loja/')
        # Verifica se a request continua com o user logado
        self.assertEqual(self.request.user, self.user)

    def test_tentativa_de_login_com_usuario_ja_logado(self):
        """Testa se um usuário conseguir mandar uma request do tipo post para a página de login
        mesmo já estando logado se o server irá retornar não autorizado e manterá o mesmo user logado"""
        # manda uma request post para a página de login
        data = {'username': 'usertest2@gmail.com', 'password': '123123123a'}
        self.request = self.factory.post('/user/login', data=data)
        self.request.user = self.user
        response = LoginClassView.as_view()(self.request)
        # Verifica se é redirecionado
        self.assertEqual(response.status_code, 302)
        # Verifica se o usuário continua logado com o user 1
        self.assertEqual(self.request.user, self.user)


class SingUpViewTest(TestCase):

    def setUp(self):
        setup_std(self, user=True)

    def test_manda_email_incorreto_no_cadastro(self):
        """Nao deve ser aceito o cadastro de usuario se o email for inválido"""
        # Manda request com email incorreto
        data = {
            'email': 'naopodecriar',
            'username': 'NaoPodeCriar',
            'first_name': 'User que',
            'last_name': 'Nao Pode Criar',
            'password1': '123123123toor',
            'password2': '123123123toor'}
        response = self.client.post('/user/signup/', data=data, follow=True)
        # Verifica se continua na página de cadastro
        self.assertTrue(mesma_pagina(response, '/user/signup/'))
        # Verifica se user foi criado
        self.assertFalse(user_existente(self, 'NaoPodeCriar'))

    def test_manda_username_muito_curto(self):
        """Nao deve ser aceito um cadastro de usuario se o username for muito curto"""
        # Manda request com username curto
        data = {
            'email': 'naopodecriar@teste.com',
            'username': 'Nao',
            'first_name': 'User que',
            'last_name': 'Nao Pode Criar',
            'password1': '123123123toor',
            'password2': '123123123toor'}
        response = self.client.post('/user/signup/', data=data, follow=True)
        # Verifica se continua na página de cadastro
        self.assertTrue(mesma_pagina(response, '/user/signup/'))
        # Verifica se user foi criado
        self.assertFalse(user_existente(self, 'Nao'))

    def test_manda_senhas_diferentes(self):
        """Nao deve ser aceito um cadastro de usuario se as senhas nao conferem"""
        # Manda request com senhas diferentes
        data = {
            'email': 'naopodecriar@teste.com',
            'username': 'NaoPodeCriar2',
            'first_name': 'User que',
            'last_name': 'Nao Pode Criar',
            'password1': '123123123toor',
            'password2': '123123123toorDIFERENTE'}
        response = self.client.post('/user/signup/', data=data, follow=True)
        # Verifica se continua na página de cadastro
        self.assertTrue(mesma_pagina(response, '/user/signup/'))
        # Verifica se o user foi criado
        self.assertFalse(user_existente(self, 'NaoPodeCriar2'))

    def test_manda_form_valido(self):
        """Quando informado um formulário válido, o usuario deve ser criado
        e redirecionado para a página de login"""
        # Manda request com informações válidas
        data = {
            'email': 'usercorreto@teste.com',
            'username': 'DeveSerCriado',
            'first_name': 'User que',
            'last_name': 'Pode Criar',
            'password1': '123123123toor',
            'password2': '123123123toor'}
        response = self.client.post('/user/signup/', data=data, follow=True)
        # Verifica se foi redirecionado para a página de login
        self.assertTrue(mesma_pagina(response, '/user/login/'))
        # Verifica se o usuário foi criado
        self.assertTrue(user_existente(self, 'DeveSerCriado'))

    def test_redireciona_usuario_ja_logado(self):
        """Se um usuário já logato tenta entrar na página de cadastro,
        deve ser redirecionado para a página de 'sua loja'"""
        # Manda uma request com um user já logado
        request = self.factory.get('/user/signup')
        request.user = self.user
        response = SignUpClassView.as_view()(request)
        # Verifica se o usuário é redirecionado para a página de 'sua loja'
        self.assertEqual(response.headers['Location'], '/sua_loja/')


class SignOutViewTest(TestCase):

    def setUp(self):
        setup_std(self, user=True)

    def test_tenta_deslogar_com_user_logado(self):
        """Primeiro faz login com user test e então realiza um logoff"""
        response = self.client.post(reverse_lazy('login_page'), {
                                    'username': 'usertest@gmail.com', 'password': '123123123a'})
        self.assertEqual(response.wsgi_request.user, self.user)
        response = self.client.get(reverse_lazy('logoff_page'))
        self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))


class UserInfoViewTest(TestCase):

    def setUp(self):
        setup_std(self, user=True)

    def test_recebe_info_correta_do_user_logado(self):
        """Com o user logado, tenta acessar a página de 'info user', deve receber informações"""
        # Login com o user test
        data = {
            'username': 'usertest@gmail.com',
            'password': '123123123a'}
        self.client.post('/user/login/', data, follow=True)
        # Faz um get na página de user info
        response = self.client.get(reverse_lazy('user_info_page'))
        # com response.content verifica se as infos do user test estão corretas
        self.assertIn(b'userTest', response.content)
        self.assertIn(b'usertest@gmail.com', response.content)
        self.assertIn(b'User', response.content)

    def test_tenta_acessar_info_sem_estar_logado(self):
        """O usuário não deve conseguir entrar na página de 'user info' sem estar logado"""
        # Faz um get na página de user info
        response = self.client.get(reverse_lazy('user_info_page'))
        # Verifica se foi redirecionado para a página de login
        self.assertEqual(response.status_code, 302)


class AlterUserInfoViewTest(TestCase):

    def setUp(self):
        setup_std(self, user=True)
        # já mantem o user test logado, já que será usado para todos os tests desta view
        data = {
            'username': 'usertest@gmail.com',
            'password': '123123123a'}
        self.client.post('/user/login/', data, follow=True)

    def test_manda_nome_em_branco(self):
        """Com o user logado, manda um post para a 'alter user info' com nome em branco,
        não deve ser aceito"""
        # Manda um post para a página de alter user info com nome em branco
        data = {
            'first_name': '',
            'last_name': 'sobrenome novo',
            'is_seller': True}
        response = self.client.post(reverse_lazy(
            'alter_user_info_page'), data=data, follow=True)
        # verifica se continua na página de alter user info
        self.assertEqual(response.wsgi_request.path_info, '/user/update/')
        # verifica se informação não foi alterada
        user = UserModel.objects.get(id=response.wsgi_request.user.id)
        self.assertEqual(user.first_name, 'User')

    def test_manda_sobrenome_em_branco(self):
        """Com o user logado, manda um post para a 'alter user info' com sobrenome em branco,
        não deve ser aceito"""
        data = {
            'first_name': 'nome novo',
            'last_name': '',
            'is_seller': True}
        response = self.client.post(reverse_lazy(
            'alter_user_info_page'), data=data, follow=True)
        # verifica se continua na página de alter user info
        self.assertEqual(response.wsgi_request.path_info, '/user/update/')
        # verifica se informação não foi alterada
        user = UserModel.objects.get(id=response.wsgi_request.user.id)
        self.assertEqual(user.last_name, 'Test')

    def test_manda_form_correto(self):
        """Com o user logado manda um form completo e correto para 'alter user info',
        deve ser aceito"""
        # Manda um post para a página de alter user info com form correto
        data = {
            'first_name': 'nome novo',
            'last_name': 'sobrenome novo',
            'is_seller': True}
        response = self.client.post(reverse_lazy(
            'alter_user_info_page'), data=data, follow=True)
        # verifica se foi redirecionado para a página de user info
        self.assertEqual(response.wsgi_request.path_info, '/user/')
        # verifica se as informações do user test foram alteradas
        user = UserModel.objects.get(id=response.wsgi_request.user.id)
        self.assertEqual(user.first_name, 'nome novo')
        self.assertEqual(user.last_name, 'sobrenome novo')
        self.assertEqual(user.is_seller, True)

    def test_acessa_pagina_sem_estar_logado(self):
        """Um user sem estar logado não deve ter acesso a página de 'alter user info'"""
        # Faz logoff
        self.client.get(reverse_lazy('logoff_page'))
        # Tenta acessar a página do alter user info
        response = self.client.get(reverse_lazy('alter_user_info_page'))
        # Verifica se foi redirecionado para tela de login
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.path_info, '/user/update/')
