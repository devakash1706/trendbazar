# Generated by Django 5.0.1 on 2024-03-06 19:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_basket_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketitem',
            name='basket_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='store.basket'),
        ),
    ]
