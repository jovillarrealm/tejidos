from django.forms import ModelForm
from .models import PatronModel
from django import forms

class PatronForm(ModelForm):
    class Meta:
        model = PatronModel
        fields = ["nombre", "detalles", "alto", "ancho", "profundidad", "precio"]

    def clean_alto(self):
        alto = self.cleaned_data["alto"]
        if alto < 0:
            raise forms.ValidationError(
                "El valor debería ser un `float` positivo :(", "invalid"
            )
        return alto

    def clean_ancho(self):
        ancho = self.cleaned_data["ancho"]
        if ancho < 0:
            raise forms.ValidationError(
                "El valor debería ser un `float` positivo :(", "invalid"
            )
        return ancho

    def clean_profundidad(self):
        profundidad = self.cleaned_data["profundidad"]
        if profundidad < 0:
            raise forms.ValidationError(
                "El valor debería ser un `float` positivo :(", "invalid"
            )
        return profundidad
    def clean_precio(self):
        profundidad = self.cleaned_data["precio"]
        if profundidad < 0:
            raise forms.ValidationError(
                "El valor debería ser un `float` positivo :(", "invalid"
            )
        return profundidad
