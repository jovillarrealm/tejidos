from django.db.models import Model
from django.db import models


# Create your models here.
class PatronModel(Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, unique=True)
    detalles = models.TextField()

    alto = models.FloatField()
    ancho = models.FloatField()
    profundidad = models.FloatField()

    precio = models.FloatField()
    descuento = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.nombre

    @property
    def precio_descuento(self) -> float:
        if self.descuento:
            return (100 - self.descuento) * self.precio / 100
        else:
            return self.precio


class ComentarioModel(Model):
    id = models.AutoField(primary_key=True)
    publicacion = models.ForeignKey(
        PatronModel, on_delete=models.CASCADE, related_name="comentarios"
    )
    autor = models.CharField(max_length=30, unique=True)
    calificacion = models.IntegerField(null=True, blank=True)
    comentario = models.TextField()
