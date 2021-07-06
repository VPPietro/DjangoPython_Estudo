from django.shortcuts import render
from django.contrib.auth import get_user
import datetime


def index_page(request):
    usuario = get_user(request)
    print(datetime.datetime.now())
    return render(request, 'index_page.html', {'usuario': usuario})
