# Generated by Django 5.0.3 on 2024-03-21 03:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amigurumi', '0005_alter_patronmodel_descuento'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComentarioModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('autor', models.CharField(max_length=30, unique=True)),
                ('calificacion', models.IntegerField(blank=True, null=True)),
                ('comentario', models.TextField()),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='amigurumi.patronmodel')),
            ],
        ),
    ]
