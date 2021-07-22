# Generated by Django 3.2.4 on 2021-07-22 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_usermodel_is_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='date_joined',
            field=models.DateField(auto_now_add=True, verbose_name='data de cadastro'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='e-mail'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='username',
            field=models.CharField(max_length=255, unique=True, verbose_name='Nome de usuário'),
        ),
    ]
