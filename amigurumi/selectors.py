from django.forms import Form
from django.http import HttpRequest

from .forms import DescuentoForm, ComentarioForm
from .models import PatronModel, ComentarioModel
from .services import make_comment

def update_item_descuento(item: PatronModel, form: Form):
    descuento = form.cleaned_data["descuento"]
    print("Dirt")
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
        print("Dirt")
        if form.is_valid():
            print("cry")
            item = PatronModel.objects.get(id=id)
            update_item_descuento(item, form)
            actions.append("descuento")
    if "comentario" in request.POST:
        form = ComentarioForm(request.POST)
        if make_comment(form, id):
            actions.append("comentario")
    return actions

def get_comments(patron:PatronModel):
    m = patron.comentarios.all()
    print(m)
    return m
    