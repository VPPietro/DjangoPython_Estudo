from apps.loja_app.models import ItensModel

def setup_std(self, kwargs, request, pk=False, item=False, permi_vend=False):
    if pk:
        self.pk = kwargs['pk'] if kwargs['pk'] else 0
    if item:
        self.item = ItensModel.objects.get(id=self.pk) if item else None
    if permi_vend:
        self.permissao_vendedor = True if self.item.vendedor == request.user else False