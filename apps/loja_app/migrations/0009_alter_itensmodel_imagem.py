# Generated by Django 3.2.4 on 2021-07-29 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja_app', '0008_alter_itensmodel_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itensmodel',
            name='imagem',
            field=models.ImageField(default='img/no_foto_item', upload_to='fotos/%Y/%m/%d/', verbose_name='Imagem do Produto'),
        ),
    ]