# Generated by Django 5.0.2 on 2024-03-01 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cardapp', '0012_alter_rulings_card'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardimage',
            name='card',
        ),
        migrations.RemoveField(
            model_name='prices',
            name='card',
        ),
        migrations.RemoveField(
            model_name='rulings',
            name='card',
        ),
    ]