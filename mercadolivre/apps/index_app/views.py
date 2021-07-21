from django.shortcuts import render
from django.contrib.auth import get_user
from loja_app.views import ItemListView


def index_page(request):
    usuario = get_user(request)
    superuser = False
    if str(usuario) != 'AnonymousUser':
        superuser = usuario.get_is_superuser()
    return render(request, 'index_page.html',
        {'usuario': usuario,
        'superuser': superuser,
        })
