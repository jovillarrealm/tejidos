from django.db.models import Model
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PatronModel(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, unique=True)
    detalles = models.TextField()

    alto = models.FloatField()

    TAMAÑO_CHOICES = [
        ("GR", "Grande"),
        ("MD", "Mediano"),
        ("PQ", "Pequeño"),
    ]
    tamaño = models.CharField(max_length=2, choices=TAMAÑO_CHOICES)

    imagen = models.ImageField(upload_to="patrones", blank=True, null=True)
    precio = models.FloatField()
    descuento = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        if self.tamaño == "GR" and not (30 <= self.alto <= 35):
            raise ValidationError(
                "La altura para el tamaño grande debe estar entre 30 y 35 cm."
            )
        elif self.tamaño == "MD" and not (25 <= self.alto <= 29):
            raise ValidationError(
                "La altura para el tamaño mediano debe estar entre 25 y 29 cm."
            )
        elif self.tamaño == "PQ" and not (20 <= self.alto <= 24):
            raise ValidationError(
                "La altura para el tamaño pequeño debe estar entre 20 y 24 cm."
            )

    @property
    def precio_descuento(self) -> float:
        if self.descuento:
            return (100 - self.descuento) * self.precio / 100
        else:
            return self.precio


class ComentarioModel(Model):
    publicacion = models.ForeignKey(
        PatronModel, on_delete=models.CASCADE, related_name="comentarios"
    )
    autor = models.CharField(max_length=30)
    calificacion = models.IntegerField(null=True, blank=True)
    comentario = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def str(self):
        return self.user.username


class CotizacionModel(Model):
    patrones_cotizados = models.ManyToManyField(PatronModel)

    @property
    def total_order(self) -> float:
        precio = 0
        for patron in self.patrones_cotizados.all():
            precio += patron.precio_descuento
        return precio


class OrderModel(Model):
    patrones = models.ManyToManyField(PatronModel)
    cotizaciones = models.ManyToManyField(CotizacionModel, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_orden(self) -> float:
        precio = 0
        for patron in self.patrones.all():
            precio += patron.precio_descuento
        for patron in self.cotizaciones.all():
            precio += patron.precio_descuento
        return precio
