from abc import ABC, abstractmethod
from itertools import batched

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from amigurumi.selectors import deal_with_PatronView_buttons
from .services import make_patron

from .forms import DescuentoForm, PatronForm
from .models import PatronModel

# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"


class CreatePatronView(View):
    template_name = "patron/crear.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = PatronForm()

        viewData = {}
        viewData["title"] = "Crear patrón de Amigurumi"
        viewData["form"] = form

        return render(request, self.template_name, viewData)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = PatronForm(request.POST)

        if make_patron(form):
            return render(request, ConfirmView.template_name)

        else:
            viewData = {}

            viewData["title"] = "Crear patrón de Amigurumi, pero bien"
            viewData["form"] = form

            return render(request, self.template_name, viewData)


class ConfirmView(View):
    template_name = "patron/confirm.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name, {})


class CatalogoListView(View):
    model = PatronModel
    template_name = "patron/catalogo.html"


class PatronView(TemplateView):
    template_name = "patron/show.html"

    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        patron = PatronModel.objects.get(id=id)
        context = {}

        context["patron"] = patron
        context["title"] = f"Amigurumis #{id} "
        context["DescuentoForm"] = DescuentoForm()
        context["DeleteForm"] = DescuentoForm()
        context["subtitle"] = "Amigurumi seleccionado"

        return render(request, self.template_name, context)

    def post(
        self, request: HttpRequest, id: int) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
        match deal_with_PatronView_buttons(request, id):
            case "delete":
                return redirect("/catalogo/")
            case "descuento"|"comentario":
                return render(request, ConfirmView.template_name)
            case _:
                return redirect("/")


class Contenedor(ABC):
    @abstractmethod
    def agregar(self):
        pass

    @abstractmethod
    def remover(self):
        pass


class CatalogoView(View):
    template_name = "patron/catalogo.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        catalogoData = PatronModel.objects.select_related().all()
        catalogo = batched(catalogoData, 3)

        viewData = {}
        viewData["catalogo"] = catalogo
        viewData["title"] = "Catálogo de Amigurumis"
        viewData["subtitle"] = "Aquí se verán los diseños prefabricados por empleados"

        return render(request, self.template_name, viewData)

    # class UsersView(ListView):
    """A menos que se especifique un `template_name`, se buscará la plantilla `patronmodel_list.html`
    porque el model es PatronModel.

    A menos que se especifique una variable `context_object_name` se podrán usar `object_list` o `patronmodel_list` dentro de la plantilla

    template_name = "model_list.html"
    context_object_name = "example_name"
    """
