# Generated by Django 5.0.3 on 2024-03-28 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_alter_cartitems_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='is_paid',
        ),
    ]
