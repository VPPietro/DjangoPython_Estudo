from django.test import TestCase


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