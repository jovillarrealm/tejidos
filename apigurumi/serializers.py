from amigurumi.models import PatronModel
from rest_framework import serializers


class PatronSerializer(serializers.ModelSerializer):
    """Serializer class for PatronModel instances."""

    class Meta:
        model = PatronModel
        fields = [
            "nombre",
            "detalles",
            "tamaño",
            "precio",
            "precio_descuento",
        ]  # Include all fields by default (customize as needed)
