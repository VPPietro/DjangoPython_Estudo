from django.shortcuts import render

from . import models



def items_list_view(request):
    itens = models.ItensModel.objects.all()
    itens_list = []
    for x in range(itens.count()):
        itens_list.append(itens[x])
    print(itens_list)
    return render(request, 'loja/list.html', {'itens': itens_list})

def items_create_view(request):
    return render(request, 'loja/create.html')