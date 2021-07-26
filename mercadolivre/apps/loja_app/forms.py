from django.forms import ModelForm, CharField, TextInput
from apps.loja_app.models import ItensModel
from apps.user_app.models import UserModel
from django.http.request import HttpRequest


class CreateItemForm(ModelForm):

    request = HttpRequest()

    def __init__(self):
        super().__init__()
        print('abc', self.request)
        self.fields['vendedor'].widget.attrs['disabled'] = True


    class Meta:
        exclude = '',
        model = ItensModel
