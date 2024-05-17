from .forms import ComentarioForm, PatronForm

def make_comment(form:ComentarioForm, id):
    """Retorna si funciona la operación con la db

    Args:
        form (ComentarioForm): el Form se usa y se valida

    Returns:
        bool: Retorna si funciona
    """
    if form.is_valid():
        form.save(id=id)
        return True
    return False


def make_patron(form: PatronForm):
    """Retorna si funciona la operación con la db

    Args:
        form (PatronForm): el Form se usa y se valida

    Returns:
        bool: Retorna si funciona
    """
    if form.is_valid():
        form.save()
        return True
    return False

