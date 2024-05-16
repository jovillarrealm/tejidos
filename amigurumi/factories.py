from .models import PatronModel, ComentarioModel, CotizacionModel
import factory
import random


class CotizacionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CotizacionModel

    @factory.post_generation
    def create_patrons(self, create, extracted, **kwargs):
        if not create:
            return
        num_patrons = random.randint(1, 10)
        for _ in range(num_patrons):
            patron = PatronFactory()


class PatronFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatronModel

    nombre = factory.Faker("company")
    detalles = factory.Faker("text")
    alto = factory.LazyFunction(lambda: 20 + round(random.random() * (35 - 20), -1))
    tamaño = random.choice(PatronModel.TAMAÑO_CHOICES)
    precio = factory.LazyFunction(lambda: round(random.random() * 1_000_000, -2))
    descuento = factory.Faker("random_int", min=0, max=99)

    @factory.post_generation
    def create_comments(self, create, extracted, **kwargs):
        if not create:
            return
        num_comments = random.randint(0, 10)
        for _ in range(num_comments):
            commentarios = ComentarioFactory(publicacion=self)


class ComentarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ComentarioModel

    publicacion = None
    autor = factory.Faker("name")
    calificacion = factory.Faker("random_int", min=1, max=5)
    comentario = factory.Faker("text")
    """
    # One to One
    @factory.post_generation
    def link_to_patron(self,create,extracted,patron=None, **kwargs):
        if not create:
            return
        if patron:
            self.patron = patron
        else:
            self.patron = PatronFactory()

        """
