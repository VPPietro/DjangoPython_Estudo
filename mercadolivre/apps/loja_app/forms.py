from typing import Text
from django.forms import ModelForm, CharField, TextInput, NumberInput, HiddenInput, FileInput
from apps.loja_app.models import ItensModel
from apps.user_app.models import UserModel
from django.http.request import HttpRequest


class CreateItemForm(ModelForm):

    request = HttpRequest()

    class Meta:
        exclude = '',
        model = ItensModel
        user = HttpRequest().get_host
        widgets = {
            'nome': TextInput(attrs={'class': 'form-control'}),
            'descricao': TextInput(attrs={'class': 'form-control'}),
            'valor': NumberInput(attrs={'class': 'form-control'}),
            'quantidade': NumberInput(attrs={'class': 'form-control'}),
            'imagem': FileInput(attrs={'class': 'form-control'}),
            'vendedor': TextInput(attrs={'value': user, 'disabled': True})
        }
