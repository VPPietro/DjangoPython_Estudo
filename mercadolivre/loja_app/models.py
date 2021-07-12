from django.db import models


class ItensModel(models.Model):

    nome = models.CharField(max_length=255, name='nome')
    descricao = models.CharField(max_length=1200, name='descricao')
    valor = models.FloatField(name='valor')
    quantidade = models.IntegerField(name='quantidade')

    class Meta:
        db_table = 'itens_model'

    def __str__(self) -> str:
        return self.nome
