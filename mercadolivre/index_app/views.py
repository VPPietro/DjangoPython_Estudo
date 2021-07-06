from django.shortcuts import render
from django.contrib.auth import get_user


def index_page(request):
    usuario = get_user(request)
    return render(request, 'index_page.html', {'usuario': usuario})
