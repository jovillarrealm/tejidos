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
    publicacion = models.ForeignKey(
        PatronModel, on_delete=models.CASCADE, related_name="comentarios"
    )
    autor = models.CharField(max_length=30, unique=True)
    calificacion = models.IntegerField(null=True, blank=True)
    comentario = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CotizacionModel(Model):
    patrones_cotizados = models.ManyToManyField(PatronModel)
    @property
    def total_orden(self) -> float:
        precio = 0
        for patron in self.patrones_cotizados.all():
            precio += patron.precio_descuento
        return precio

class OrderModel(Model):
    patrones = models.ManyToManyField(PatronModel)
    cotizaciones = models.ManyToManyField(CotizacionModel)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def total_orden(self) -> float:
        precio = 0
        for patron in self.patrones.all():
            precio += patron.precio_descuento
        for patron in self.cotizaciones.all():
            precio += patron.precio_descuento
        return precio
