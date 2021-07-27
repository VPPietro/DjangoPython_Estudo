from django.forms import ModelForm, TextInput, NumberInput, HiddenInput, FileInput, Textarea
from apps.loja_app.models import ItensModel


class CreateItemForm(ModelForm):

    class Meta:

        exclude = '',
        model = ItensModel
        widgets = {
            'nome': TextInput(attrs={'class': 'form-control'}),
            'descricao': Textarea(attrs={'class': 'form-control'}),
            'valor': NumberInput(attrs={'class': 'form-control'}),
            'quantidade': NumberInput(attrs={'class': 'form-control'}),
            'imagem': FileInput(attrs={'class': 'form-control'}),
            'vendedor': HiddenInput(),
        }
