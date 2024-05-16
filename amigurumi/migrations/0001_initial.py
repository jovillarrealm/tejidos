# Generated by Django 5.0.4 on 2024-05-03 19:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CotizacionModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PatronModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=30, unique=True)),
                ("detalles", models.TextField()),
                ("alto", models.FloatField()),
                (
                    "tamaño",
                    models.CharField(
                        choices=[
                            ("GR", "Grande"),
                            ("MD", "Mediano"),
                            ("PQ", "Pequeño"),
                        ],
                        max_length=2,
                    ),
                ),
                (
                    "imagen",
                    models.ImageField(blank=True, null=True, upload_to="patrones"),
                ),
                ("precio", models.FloatField()),
                ("descuento", models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="OrderModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "cotizaciones",
                    models.ManyToManyField(null=True, to="amigurumi.cotizacionmodel"),
                ),
                ("patrones", models.ManyToManyField(to="amigurumi.patronmodel")),
            ],
        ),
        migrations.AddField(
            model_name="cotizacionmodel",
            name="patrones_cotizados",
            field=models.ManyToManyField(to="amigurumi.patronmodel"),
        ),
        migrations.CreateModel(
            name="ComentarioModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("autor", models.CharField(max_length=30)),
                ("calificacion", models.IntegerField(blank=True, null=True)),
                ("comentario", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "publicacion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comentarios",
                        to="amigurumi.patronmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
