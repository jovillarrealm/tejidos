from django.forms import ModelForm, Form
from .models import PatronModel, ComentarioModel
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PatronForm(ModelForm):
    class Meta:
        model = PatronModel
        fields = [
            "nombre",
            "detalles",
            "alto",
            "imagen",
            "precio",
            "descuento",
        ]
        """
        labels = {
            'nombre': 'Nombre completo',
            "detalles": "Especificar detalles del patron",
            "alto":"Ingresar alto (cm)",
            "imagen":"Cargue la imagen",
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

            if not (0 <= descuento <= 100 and int(descuento) == descuento):
                raise forms.ValidationError(
                    "El valor debería ser un `int` positivo :(", "invalid"
                )
            else:
                return descuento
        return 0


class DescuentoForm(Form):
    descuento = forms.IntegerField(max_value=100, min_value=0, required=True)

    def clean_descuento(self):
        descuento_n = "descuento"
        if descuento_n in self.cleaned_data:
            descuento: int = self.cleaned_data[descuento_n]

            if not (0 <= descuento <= 100 and int(descuento) == descuento):
                raise forms.ValidationError(
                    "El valor debería ser un `int` positivo :(", "invalid"
                )
            else:
                return descuento
        return 0


class ComentarioForm(ModelForm):
    class Meta:
        model = ComentarioModel
        fields = "__all__"
        exclude = ("publicacion",)

    def clean_calificación(self):
        cali_n = "calificación"
        if cali_n in self.cleaned_data:
            calificacion: int = self.cleaned_data[cali_n]
        if not (
            calificacion
            and 1 <= calificacion <= 5
            and int(calificacion) == calificacion
        ):
            raise forms.ValidationError(
                "El valor debería ser un `int` positivo :(", "invalid"
            )
        else:
            return calificacion

    def save(self, id, commit=True):
        instance = super().save(commit=False)
        instance.publicacion = PatronModel.objects.get(pk=id)
        if commit:
            instance.save()
        return instance


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kargs):
        super(RegisterForm, self).__init__(*args, **kargs)
        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({"class": "form-control"})
