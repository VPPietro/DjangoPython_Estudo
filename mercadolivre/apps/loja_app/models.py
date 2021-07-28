from django.db import models
from django.db.models.deletion import CASCADE
from apps.user_app.models import UserModel


class ItensModel(models.Model):

    nome = models.CharField(max_length=255, name='nome')
    descricao = models.CharField(max_length=1200, name='descricao')
    valor = models.FloatField(name='valor')
    quantidade = models.IntegerField(name='quantidade')
    vendedor = models.ForeignKey(UserModel, on_delete=CASCADE)
    imagem = models.ImageField(verbose_name='Imagem do Produto', upload_to='fotos/%Y/%m/%d/')

    class Meta:
        db_table = 'itens_model'

    def __str__(self) -> str:
        return self.nome

    def get_id(self):
        return self.id
