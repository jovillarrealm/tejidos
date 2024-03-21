from django.forms import Form
from django.http import HttpRequest

from .forms import DescuentoForm, ComentarioForm
from .models import PatronModel, ComentarioModel
from .services import make_comment

def update_item_descuento(item: PatronModel, form: Form):
    descuento = form.cleaned_data["descuento"]
    item.descuento = descuento
    item.save()


def deal_with_PatronView_buttons(request: HttpRequest, id: int):
    if "delete" in request.POST:
        PatronModel.objects.get(id=id).delete()
        if not PatronModel.objects.filter(id=id).exists():
            return "delete"
    elif "descuento" in request.POST:
        form = DescuentoForm(request.POST)
        if form.is_valid():
            item = PatronModel.objects.get(id=id)
            update_item_descuento(item, form)
            return "descuento"
    elif "comentario" in request.POST:
        form = ComentarioForm(request.POST)
        if make_comment(form):
            return "comentario"
    return "error"
