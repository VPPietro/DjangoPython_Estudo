from apps.user_app.models import UserModel


# Username
def comprimento_minimo_username(username: str, lista_de_erros: dict):
    """Verifica se username informado tem o comprimento mínimo necessário"""
    if len(username) <= 4:
        lista_de_erros['username'].append('Nome de usuário muito curto, mínimo 5 caracteres.')


def verifica_username_existente(username: str, lista_de_erros: dict, ):
    user = UserModel.objects.filter(username=username)
    if user:
        lista_de_erros['username'].append('Nome de Usuário já cadastrado')


# Email
def verifica_email_existente(email: str, lista_de_erros: dict):
    email = UserModel.objects.filter(email=email)
    if email:
        lista_de_erros['email'].append('E-mail já cadastrado')
        return True
    return False
