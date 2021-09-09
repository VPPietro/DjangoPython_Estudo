# Generated by Django 3.2.4 on 2021-09-09 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart_app', '0009_alter_cartitemmodel_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitemmodel',
            name='comprador',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
