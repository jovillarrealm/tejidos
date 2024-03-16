from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpRequest
from abc import ABC, abstractmethod
from .forms import PatronForm
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

            viewData["title"] = "Create product"

            viewData["form"] = form

            return render(request, self.template_name, viewData)

class ConfirmIngresoView(View):
    template_name = "patron/ingreso.html"

    def post(self, request):

        return render(request, self.template_name, {})
class CatalogoView(View):
    template_name = "patron/catalogo.html"
    def get(self, request):
        
        catalogoData = PatronModel.objects.select_related().all()
        viewData={}
        viewData["catalogo"] = catalogoData
        viewData["title"] = "Catálogo de Amigurumis"
        viewData["subtitle"] = "Aquí se verán los diseños prefabricados por empleados"

        return render(request,self.template_name,viewData)


class PatronView(TemplateView):
    template_name = "patron/mostrar.html"

    def get(self, request, id):
        context = {}
        context["product"] = PatronModel.objects.get(id=id)
        context["title"] = f"Amigurumis #{id} "
        context["subtitle"] = "Amigurumi seleccionado"
        return render(request, self.template_name,context)
    
    def post(self, request, id):
        print(id)
        PatronModel.objects.filter(id=id).delete()
        if not PatronModel.objects.filter(id=id).exists():
            return redirect("/catalogo/")
        
        

        



class Contenedor(ABC):
    @abstractmethod
    def agregar(self):
        pass
    
    @abstractmethod
    def remover(self):
        pass