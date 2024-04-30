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


def split_chunks(data, chunk_size: int = 4):
    """
    Splits a list into chunks of a specified size.

    Args:
        data: The list to be split.
        chunk_size: The desired size of each chunk.

    Returns:
        A list of lists, where each sublist is a chunk of the original list.
    """
    chunks = []
    current_chunk = []
    for item in data:
        current_chunk.append(item)
        if len(current_chunk) == chunk_size:
            chunks.append(current_chunk)
            current_chunk = []
    # Append the remaining items even if they don't fill a chunk
    if current_chunk:
        chunks.append(current_chunk)
    return chunks
