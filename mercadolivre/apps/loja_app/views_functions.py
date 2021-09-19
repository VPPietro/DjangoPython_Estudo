from apps.loja_app.models import ItensModel
from django.core.exceptions import ObjectDoesNotExist


def tem_permissao_de_alteracao(request, kwargs):
    """Retorna True caso tenha permissão, se não False"""
    item_id = kwargs.get('pk', None)
    user_id = request.user.id
    try: item = ItensModel.objects.select_related().get(id=item_id)
    except ObjectDoesNotExist: return False
    if item.vendedor_id == user_id:
        return True
    else:
        return False
