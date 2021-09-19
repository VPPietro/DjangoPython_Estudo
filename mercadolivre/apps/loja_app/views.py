from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.http.response import HttpResponseRedirect, HttpResponseBase
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from apps.loja_app.views_functions import *
from apps.loja_app.forms import CreateItemForm, UpdateItemForm

decorator = [
    login_required(login_url=reverse_lazy('login_page')),
    permission_required(login_url=reverse_lazy('lista-itens-user'), perm='user_app.has_perm')
]


class ItemListView(ListView):

    model = ItensModel
    template_name = 'loja/list.html'
    paginate_by = 10
    context_object_name = 'itens'
    ordering = ['-id']  # item mais recente primeiro


class ItemDetailView(DetailView):
    model = ItensModel
    template_name = 'loja/detail.html'
    context_object_name = 'item'


@method_decorator(decorator, name='dispatch')
class ItemCreateView(SuccessMessageMixin, CreateView):

    model = ItensModel
    template_name = 'loja/create.html'
    success_url = reverse_lazy('lista-itens-user')
    success_message = 'Produto cadastrado com sucesso'
    form_class = CreateItemForm

    def get_initial(self):
        """Set initial values for fields"""
        self.initial = {'vendedor': self.request.user.id}
        return super().get_initial()

    def form_valid(self, form: CreateItemForm) -> HttpResponse:
        # Camada de segurança, impedir que usuário altere hiddenfield 'vendedor'
        if self.request.POST['vendedor'] != str(self.request.user.id):
            messages.error(self.request, 'Erro de formulário, tente novamente')
            return redirect('criar-itens')
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, 'Formulário inválido, corrija os erros abaixo')
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class ItemUpdateView(UpdateView):
    model = ItensModel
    template_name = 'loja/update.html'
    context_object_name = 'item'
    form_class = UpdateItemForm
    success_url = '/sua_loja/'

    def dispatch(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponseBase:
        """Não permite que acesse a página de alteração caso não seja dono do item"""
        if not tem_permissao_de_alteracao(request, kwargs):
            messages.error(self.request, 'Você não tem permissão para alterar este item')
            return HttpResponseRedirect(reverse_lazy('lista-itens-user'))
        return super().dispatch(request, *args, **kwargs)


@method_decorator(decorator, name='dispatch')
class ItemDeleteView(DeleteView):
    model = ItensModel
    template_name = 'loja/delete.html'
    success_url = reverse_lazy('lista-itens-user')
    context_object_name = 'object'

    def dispatch(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponseBase:
        """Não permite que acesse a página de deletar caso não seja dono do item"""
        if not tem_permissao_de_alteracao(request, kwargs):
            messages.error(request, 'Você não tem permissão para deletar este item')
            return HttpResponseRedirect(reverse_lazy('lista-itens-user'))
        return super().dispatch(request, *args, **kwargs)
