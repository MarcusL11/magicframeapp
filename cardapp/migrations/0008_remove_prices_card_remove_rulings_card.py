# Generated by Django 5.0.2 on 2024-03-01 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cardapp', '0007_remove_cardimage_card'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prices',
            name='card',
        ),
        migrations.RemoveField(
            model_name='rulings',
            name='card',
        ),
    ]
