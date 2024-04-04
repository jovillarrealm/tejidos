from django.forms import Form
from django.http import HttpRequest

from .forms import ComentarioForm, DescuentoForm
from .models import ComentarioModel, PatronModel
from .services import make_comment


def update_item_descuento(item: PatronModel, form: Form):
    descuento = form.cleaned_data["descuento"]
    item.descuento = descuento
    item.save()


def deal_with_PatronView_buttons(request: HttpRequest, id: int):
    actions = []
    if "delete" in request.POST:
        PatronModel.objects.get(id=id).delete()
        if not PatronModel.objects.filter(id=id).exists():
            actions.append("delete")
    if "descuento" in request.POST:
        form = DescuentoForm(request.POST)
        if form.is_valid():
            item = PatronModel.objects.get(id=id)
            update_item_descuento(item, form)
            actions.append("descuento")
    if "comentario" in request.POST:
        form = ComentarioForm(request.POST)
        if make_comment(form, id):
            actions.append("comentario")
    return actions


def get_comments(patron: PatronModel):
    return patron.comentarios.all()  # type: ignore


def get_top_comentarios():  # type: ignore
    try:
        # Obtener los tres comentarios mejor calificados con calificación no nula
        top_comentarios = ComentarioModel.objects.exclude(calificacion=None).order_by(
            "-calificacion"
        )[:3]
    except ComentarioModel.DoesNotExist:
        # Manejar el caso en el que no se encuentren comentarios
        top_comentarios = None
    return top_comentarios  # type: ignore
