from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from amigurumi.selectors import (
    deal_with_PatronView_buttons,
    get_comments,
    get_top_comentarios,
    get_catalogoData,
    split_chunks,
    ReporteXlsx,
    ReporteArrow,
)

from .forms import ComentarioForm, DescuentoForm, PatronForm, RegisterForm
from .models import PatronModel, UserProfile
from .services import make_patron
from .interface import Reporte

# Create your views here.


def home(request):
    return render(request, "home.html")


class CreatePatronView(LoginRequiredMixin, View):
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
        self, request: HttpRequest, id: int
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
        match deal_with_PatronView_buttons(request, id):
            case ["delete", *_]:
                return redirect("/catalogo/")
            case ["descuento" | "comentario", *_]:
                return render(request, ConfirmView.template_name)
            case _:
                return redirect("home")


class CatalogoView(View):
    template_name = "patron/catalogo.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        catalogoData = get_catalogoData()
        catalogo_rows = split_chunks(catalogoData)
        viewData = {}
        viewData["catalogo_rows"] = catalogo_rows
        viewData["title"] = "Catálogo de Amigurumis"
        viewData["subtitle"] = "Aquí se verán los diseños prefabricados por empleados"

        return render(request, self.template_name, viewData)


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")


def RegisterPage(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()

                UserProfile.objects.create(user=user)

                login(request, user)
                return redirect("home")
            except IntegrityError:
                return render(
                    request,
                    "users/register.html",
                    {
                        "form": form,
                        "error": "Username already taken. Choose a new username.",
                    },
                )
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def LogoutView(request):
    logout(request)
    return redirect("home")


def topcomentarios(request):
    top_comentarios = get_top_comentarios()
    context = {"top_comentarios": top_comentarios}
    return render(request, "home.html", context)


class ReporteView(View):
    def get(self, request, format: str):
        match format:
            case "excel":
                reporte: Reporte = ReporteXlsx()
            case "arrow":
                reporte: Reporte = ReporteArrow()
            case _:
                return redirect("catalogo")
        catalogoData = get_catalogoData()
        return reporte.reportar(catalogoData)

class AliadosIframeView(TemplateView):
    template_name = "patron/aliadosiframe.html"

class AliadosView(View):
    template_name = "patron/aliadosmain.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        catalogoData = ()
        catalogo_rows = split_chunks(catalogoData)
        viewData = {}
        viewData["catalogo_rows"] = catalogo_rows
        viewData["title"] = "Catálogo de Amigurumis"
        viewData["subtitle"] = "Aquí se verán los diseños prefabricados por empleados"

        return render(request, self.template_name, viewData)