from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ItensModel
from apps.loja_app.forms import CreateItemForm


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


class ItemDetailView(DetailView):
    model = ItensModel
    template_name = 'loja/detail.html'
    context_object_name = 'item'


decorators = [
    permission_required(login_url='/user/login', perm='user_app.has_perm')
    ]


@method_decorator(decorators, name='dispatch')
class ItemCreateView(CreateView):

    model = ItensModel
    template_name = 'loja/create.html'
    fields = ('vendedor', 'nome', 'descricao', 'valor', 'quantidade', 'imagem')
    success_url = reverse_lazy('lista-itens-user')

    def get_initial(self) -> dict[str, any]:
        """Set initial values for fields"""
        self.initial = {'vendedor': self.request.user.id}
        return super().get_initial()

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        return CreateItemForm(**self.get_form_kwargs())

    def form_valid(self, form: CreateItemForm) -> HttpResponse:
        form = CreateItemForm(self.request.POST, self.request.FILES)
        # Camada de segurança, impedir que usuário altere hiddenfield 'vendedor'. tem q criar mensagem?
        if self.request.POST['vendedor'] != str(self.request.user.id):
            print('deu erro de vendedor')
            return redirect('criar-itens')
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        print('form invalido', self.request.FILES)
        form = CreateItemForm(self.request.POST, self.request.FILES)
        return self.render_to_response(self.get_context_data(form=form))

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
