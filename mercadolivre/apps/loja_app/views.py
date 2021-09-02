from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from apps.loja_app.views_func import *
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
class ItemUpdateView(UpdateView):  # A foto do item não atualiza
    model = ItensModel
    template_name = 'loja/update.html'
    context_object_name = 'item'
    form_class = UpdateItemForm
    success_url = '/sua_loja/'
    extra_context = {}

    def setup(self, request: HttpRequest, *args: any, **kwargs: any) -> None:
        """Inclui foto do item para visualização da foto atual"""
        imagem = ItensModel.objects.get(id=kwargs['pk']).imagem
        self.extra_context['foto'] = '/media/' + str(imagem)
        setup_std(self, kwargs, request, pk=True, item=True, permi_vend=True)
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs: any):
        """Camada de segurança que não permite o vendedor alterar qualquer item que não seja dele."""
        self.context = super().get_context_data(**kwargs)
        if self.context['item'].vendedor.id != self.request.user.id:
            messages.error(self.request, 'Você não tem permissão para alterar este item')
            return {}
        return self.context

    def post(self, request: HttpRequest, *args: str, **kwargs: any) -> HttpResponse:
        if not self.permissao_vendedor:
            messages.error(self.request, 'Você não tem permissão para alterar este item')
            return HttpResponseRedirect(reverse_lazy('index_page'))
        return super().post(request, *args, **kwargs)


@method_decorator(decorator, name='dispatch')
class ItemDeleteView(DeleteView):
    model = ItensModel
    template_name = 'loja/delete.html'
    success_url = reverse_lazy('lista-itens-user')
    context_object_name = 'object'

    def setup(self, request: HttpRequest, *args: any, **kwargs: any) -> None:
        setup_std(self, kwargs, request, pk=True, item=True, permi_vend=True)
        return super().setup(request, *args, **kwargs)

    # Remove contexto da request caso o vendedor não tenha permissão
    def get_context_data(self, **kwargs: any):
        if not self.permissao_vendedor:
            return {}
        return super().get_context_data(**kwargs)

    # Não permite deletar item que não seja do vendedor
    def delete(self, request, *args, **kwargs):
        if not self.permissao_vendedor:
            messages.error(request, 'Você não tem permissão para deletar este item')
            return HttpResponseRedirect(reverse_lazy('index_page'))
        return super().delete(self, request, *args, **kwargs)
