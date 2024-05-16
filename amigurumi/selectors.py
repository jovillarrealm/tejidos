import io
from django.forms import Form
from django.http import FileResponse, HttpRequest

from .forms import ComentarioForm, DescuentoForm
from .models import ComentarioModel, PatronModel
from .services import make_comment
from .interface import Reporte
# Exclusively for ReporteXlsx
import xlsxwriter
from datetime import date 
import requests
from django.http import JsonResponse
# For ReporteArrow
import pyarrow as pa

import pyarrow.feather as feather



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


def get_catalogoData():
    return PatronModel.objects.select_related().all()


class ReporteXlsx(Reporte):
    def __init__(self, **kwargs):
        pass

    def build_excel(self,data, path):
        buffer = io.BytesIO()
        wb = xlsxwriter.Workbook(buffer)
        ws = wb.add_worksheet()
        bold = wb.add_format({'bold': True})
        row_i, col_i = 0,0
        ws.write_row(row_i,col_i,["Nombre", "Tamaño", "Precio", "Precio en descuento", date.today().strftime("%d/%m/%Y") ], bold)
        for row in data:
            row_i +=1
            ws.write_row(row_i,col_i, row)
        wb.close()
        buffer.seek(0)
        return buffer


    def reportar(self, data, path="static/amigurumi/amigurumi.xlsx"):
        result = []
        for p in data:
            p = (p.nombre, p.tamaño, p.precio, p.precio_descuento)
            result.append(p)
        buffer = self.build_excel(result, path)
        return FileResponse(buffer,as_attachment=True, filename="catalogo.xlsx")




class ReporteArrow(Reporte):
    def __init__(self, **kwargs):
        self.today = date.today().strftime("%d/%m/%Y")

    def build_file(self, data):
        # Define data types for each column
        data_types = [
            pa.string(),  # 'Company Name'
            pa.string(),  # 'Industry'
            pa.float32(),  # 'Sales'
            pa.float32(),  # 'Profit'
        ]

        # Create PyArrow arrays from data
        arrays = []
        for i in range(len(data_types)):
            column_data = [row[i] for row in data]
            arrays.append(pa.array(column_data, type=data_types[i]))

        # Build schema from field names and types
        schema = pa.schema([("Nombre", arrays[0].type), ("Tamaño", arrays[1].type), ("Precio", arrays[2].type), ("Precio en descuento", arrays[3].type)])

        # Create a PyArrow table from arrays and schema
        table: pa.Table = pa.Table.from_arrays(arrays, schema=schema)
        buffer = io.BytesIO()
        feather.write_feather(table,buffer)
        buffer.seek(0)
        return buffer
        # Create a Django response object, and specify content_type as pdf

    def reportar(self, data):
        result = []
        for p in data:
            p = (p.nombre, p.tamaño, p.precio, p.precio_descuento)
            result.append(p)
        response = self.build_file(result)
        return FileResponse(response, content_type='binary/octet-stream', filename="catalogo.arrow")

def consume_api(url= "http://countrybox.online:8000/product/countrybox-api/"):
    response = requests.get(url)
    data = response.json()
    print(data)
    return data


