from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ItensModel


class ItemListView(ListView):

    model = ItensModel
    template_name = 'loja/list.html'
    paginate_by = 10
    context_object_name = 'itens'
    ordering = ['-id']  # item mais recente primeiro

    def get_context_data(self, *, object_list=None, **kwargs):
        """Herdando do get context Data padrão + acrescentando quantidade de itens mostrado
        por coluna na index e dashboard"""
        # Herdando o context original:
        context = super(ItemListView, self).get_context_data(**kwargs)
        print(context)
        return context
        # Separando itens em listas dentro da lista original de context['itens']
        # quantidade_por_linha = 10
        # lista_parcial = []
        # start = -quantidade_por_linha
        # for i in range(int(len(context['itens']) / quantidade_por_linha) + 1):
        #     start = start + quantidade_por_linha
        #     end = start + quantidade_por_linha
        #     lista_parcial.append(context['itens'][start:end])
        # context['itens'] = lista_parcial
        # print(context)
        # return context

        # ** CASO PRECISE ADICIONAR UM PAGINADOR **
        # itens = self.get_queryset()
        # page = self.request.GET.get('page')
        # paginator = Paginator(itens, self.paginate_by)
        # try:
        #     itens = paginator.page(page)
        # except PageNotAnInteger:
        #     itens = paginator.page(1)
        # except EmptyPage:
        #     itens = paginator.page(paginator.num_pages)
        # context['itens'] = itens
        # return context


decorators = [
    permission_required(login_url='/user/login', perm='user_app.hasperm')
    ]


@method_decorator(decorators, name='dispatch')
class ItemCreateView(CreateView):
    # initial = {'vendedor': }
    model = ItensModel
    template_name = 'loja/create.html'
    fields = ('nome', 'descricao', 'valor', 'quantidade', 'vendedor')
    success_url = reverse_lazy('lista-itens-user')


# class ItemCreation(CreateView):
#     initial = {'size': 'L'}
#     model = ItensModel
#     success_url = reverse_lazy('items:index')
#
#     def get_initial(self):
#         initial_base = super(ItemCreation, self).get_initial()
#         initial_base['menu'] = ItensModel.objects.get(id=1)
#         return initial_base


class ItemDetailView(DetailView):
    model = ItensModel
    template_name = 'loja/detail.html'
    context_object_name = 'item'


@method_decorator(decorators, name='dispatch')
class ItemUpdateView(UpdateView):
    model = ItensModel
    template_name = 'loja/update.html'
    context_object_name = 'item'
    fields = ('nome', 'descricao', 'valor', 'quantidade')

    def get_success_url(self) -> str:
        return reverse_lazy('detalhe-itens', kwargs={'pk': self.object.id})


@method_decorator(decorators, name='dispatch')
class ItemDeleteView(DeleteView):
    model = ItensModel
    template_name = 'loja/delete.html'
    success_url = reverse_lazy('lista-itens')
