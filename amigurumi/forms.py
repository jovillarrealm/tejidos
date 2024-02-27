
from django import forms

class ProductForm(forms.Form):
    

    name = forms.CharField(required=True)
    detalles = forms.CharField(required=True)

    alto = forms.FloatField(required=True)
    ancho = forms.FloatField(required=True)
    profundidad = forms.FloatField(required=True)



    def clean_alto(self):
        alto = self.cleaned_data["alto"]
        if alto < 0:
            raise forms.ValidationError("El valor debería ser un `float` positivo :(", "invalid")
        return alto
    def clean_ancho(self):
        ancho = self.cleaned_data["ancho"]
        if ancho < 0:
            raise forms.ValidationError("El valor debería ser un `float` positivo :(", "invalid")
        return ancho
    def clean_profundidad(self):
        profundidad = self.cleaned_data["profundidad"]
        if profundidad < 0:
            raise forms.ValidationError("El valor debería ser un `float` positivo :(", "invalid")
        return profundidad