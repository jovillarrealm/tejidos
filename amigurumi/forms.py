from django.forms import ModelForm, Form
from .models import PatronModel  # , ComentarioModel
from django import forms


class PatronForm(ModelForm):
    class Meta:
        model = PatronModel
        fields = [
            "nombre",
            "detalles",
            "alto",
            "ancho",
            "profundidad",
            "precio",
            "descuento",
        ]
        """
        labels = {
            'nombre': 'Nombre completo',
            "detalles": "Especificar detalles del patron",
            "alto":"Ingresar alto (cm)",
            "ancho":"Ingresar ancho (cm)",
            "profundidad":"Ingresar profundidad (cm)",
            "precio":"Ingresar precio (COP)",
            "descuento": "Ingresar descuento de precio (%)",
        }
        """

    def clean_alto(self):
        alto = self.cleaned_data["alto"]
        if alto <= 0:
            raise forms.ValidationError(
                "El valor debería ser un `float` positivo :(", "invalid"
            )
        return alto

    def clean_ancho(self):
        ancho = self.cleaned_data["ancho"]
        if ancho <= 0:
            raise forms.ValidationError(
                "El valor debería ser un `float` positivo :(", "invalid"
            )
        return ancho

    def clean_profundidad(self):
        profundidad = self.cleaned_data["profundidad"]
        if profundidad <= 0:
            raise forms.ValidationError(
                "El valor debería ser un `float` positivo :(", "invalid"
            )
        return profundidad

    def clean_precio(self):
        precio = self.cleaned_data["precio"]
        if precio <= 0:
            raise forms.ValidationError(
                "El valor debería ser un `float` positivo :(", "invalid"
            )
        return precio

    def clean_descuento(self):
        descuento_n = "descuento"
        if descuento_n in self.cleaned_data:
            descuento: int = self.cleaned_data[descuento_n]
        if not (descuento and 0 <= descuento <= 100 and int(descuento) == descuento):
            raise forms.ValidationError(
                "El valor debería ser un `int` positivo :(", "invalid"
            )
        else:
            return descuento


class DescuentoForm(Form):
    descuento = forms.IntegerField(max_value=100, min_value=0, required=True)

    def clean_descuento(self):
        descuento_n = "descuento"
        if descuento_n in self.cleaned_data:
            descuento: int = self.cleaned_data[descuento_n]
        if not (descuento and 0 <= descuento <= 100 and int(descuento) == descuento):
            raise forms.ValidationError(
                "El valor debería ser un `int` positivo :(", "invalid"
            )
        else:
            return descuento


"""
class ComentarioForm(ModelForm):
    class Meta:
        model = ComentarioModel
        fields = [
            "nombre",
            "detalles",
            "alto",
            "ancho",
            "profundidad",
            "precio",
            "descuento",
        ]
    """
