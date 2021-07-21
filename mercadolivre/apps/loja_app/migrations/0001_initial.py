# Generated by Django 3.2.4 on 2021-07-12 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItensModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome do Item', models.CharField(max_length=255)),
                ('Descrição do Item!', models.CharField(max_length=1200)),
                ('Valor do Item', models.FloatField()),
                ('Quantidade de Itens', models.IntegerField()),
            ],
            options={
                'db_table': 'itens_model',
            },
        ),
    ]
