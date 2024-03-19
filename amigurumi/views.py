from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView
from django.http import HttpRequest
from abc import ABC, abstractmethod
from .forms import PatronForm, DescuentoForm
from .models import PatronModel

# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"


class CreatePatronView(View):
    template_name = "patron/crear.html"

    def get(self, request):
        form = PatronForm()

        viewData = {}
        viewData["title"] = "Crear patrón de Amigurumi"
        viewData["form"] = form

        return render(request, self.template_name, viewData)

    def post(self, request: HttpRequest):
        form = PatronForm(request.POST)

        if form.is_valid():
            form.save()

            return render(request, ConfirmIngresoView.template_name)

        else:
            viewData = {}

            viewData["title"] = "Crear patrón de Amigurumi, pero bien"
            viewData["form"] = form

            return render(request, self.template_name, viewData)


class ConfirmIngresoView(View):
    template_name = "patron/ingreso.html"

    def post(self, request):
        return render(request, self.template_name, {})


class CatalogoListView(View):
    model = PatronModel
    template_name = "patron/catalogo.html"


class PatronView(TemplateView):
    template_name = "patron/show.html"

    def get(self, request: HttpRequest, id):
        patron = PatronModel.objects.get(id=id)
        context = {}

        context["patron"] = patron
        context["title"] = f"Amigurumis #{id} "
        context["DescuentoForm"] = DescuentoForm()
        context["DeleteForm"] = DescuentoForm()
        context["subtitle"] = "Amigurumi seleccionado"

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, id):
        if "delete" in request.POST:
            PatronModel.objects.get(id=id).delete()

            if not PatronModel.objects.filter(id=id).exists():
                return redirect("/catalogo/")
        elif "descuento" in request.POST:
            form = DescuentoForm(request.POST)

            if form.is_valid():
                descuento = form.cleaned_data["descuento"]
                item = PatronModel.objects.get(id=id)
                item.descuento = descuento
                item.save()

                return render(request, ConfirmIngresoView.template_name)


class Contenedor(ABC):
    @abstractmethod
    def agregar(self):
        pass

    @abstractmethod
    def remover(self):
        pass


class CatalogoView(View):
    template_name = "patron/catalogo.html"

    def get(self, request):
        catalogoData = PatronModel.objects.select_related().all()
        viewData = {}
        viewData["catalogo"] = catalogoData
        viewData["title"] = "Catálogo de Amigurumis"
        viewData["subtitle"] = "Aquí se verán los diseños prefabricados por empleados"

        return render(request, self.template_name, viewData)


class UsersView(ListView):
    """A menos que se especifique un `template_name`, se buscará la plantilla `patronmodel_list.html`
    porque el model es PatronModel.

    A menos que se especifique una variable `context_object_name` se podrán usar `object_list` o `patronmodel_list` dentro de la plantilla

    template_name = "model_list.html"
    context_object_name = "example_name"
    """
