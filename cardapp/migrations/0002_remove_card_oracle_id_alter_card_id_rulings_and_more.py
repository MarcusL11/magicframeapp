# Generated by Django 5.0.2 on 2024-02-29 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='oracle_id',
        ),
        migrations.AlterField(
            model_name='card',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Rulings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=100)),
                ('published_at', models.DateField()),
                ('comment', models.TextField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rulings', to='cardapp.card')),
            ],
        ),
        migrations.DeleteModel(
            name='Ruiling',
        ),
    ]
