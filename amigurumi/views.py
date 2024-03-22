from abc import ABC, abstractmethod

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import models, IntegrityError
from django.db.models import Avg
from .forms import RegisterForm

from amigurumi.selectors import deal_with_PatronView_buttons, get_comments
from .services import make_patron

from .forms import DescuentoForm, PatronForm, ComentarioForm
from .models import PatronModel,ComentarioModel, UserProfile

# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"


class CreatePatronView(LoginRequiredMixin,View):
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
    template_name = "patron/catalogo.html"
    model = PatronModel


class PatronView(TemplateView):
    template_name = "patron/show.html"

    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        patron = PatronModel.objects.get(id=id)
        context = {}

        context["patron"] = patron
        context["title"] = f"Amigurumis #{id} "
        context["DescuentoForm"] = DescuentoForm()
        context["DeleteForm"] = DescuentoForm()
        context["ComentarioForm"] = ComentarioForm()
        context["comentarios"] = get_comments(patron)
        context["subtitle"] = "Amigurumi seleccionado"

        return render(request, self.template_name, context)

    def post(
        self, request: HttpRequest, id: int) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
        match deal_with_PatronView_buttons(request, id):
            case ["delete", *_]:
                return redirect("/catalogo/")
            case ["descuento"|"comentario", *rest]:
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
        catalogo = catalogoData

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

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')

def RegisterPage(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                
                UserProfile.objects.create(user=user)

                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'users/register.html', {'form': form, 'error': 'Username already taken. Choose a new username.'})
    else:
        form = RegisterForm()
    return render(request, 'users/register.html',{'form': form})

def LogoutView(request):
    logout(request)
    return redirect('http://localhost:8000/')

def topcomentarios(request):
    try:
        # Obtener los tres comentarios mejor calificados con calificación no nula
        top_comentarios = ComentarioModel.objects.exclude(calificacion=None).order_by('-calificacion')[:3]
    except ComentarioModel.DoesNotExist:
        # Manejar el caso en el que no se encuentren comentarios
        top_comentarios = []

    context = {
        'top_comentarios': top_comentarios
    }
    return render(request, 'home.html', context)
