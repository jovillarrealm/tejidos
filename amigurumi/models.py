from django.db.models import Model
from django.db import models
# Create your models here.
class PatronModel(Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 30 ,unique=True)
    detalles = models.TextField()

    alto = models.FloatField()
    ancho = models.FloatField()
    profundidad = models.FloatField()
    precio = models.FloatField()
    def __str__(self):
        return self.nombre
