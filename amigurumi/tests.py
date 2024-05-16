from django.test import TestCase
from .models import PatronModel, ComentarioModel
from .factories import PatronFactory, ComentarioFactory


class PatronModelTest(TestCase):
    def test_create_patron(self):
        """Tests creating a new Patron using the factory"""
        patron = PatronFactory()
        patron.save()
        self.assertIsNotNone(patron.pk)  # Assert that a primary key is assigned

    def test_read_patron(self):
        """Tests retrieving an existing Patron"""
        patron = PatronFactory()
        patron.save()

        retrieved_patron = PatronModel.objects.get(pk=patron.pk)
        self.assertEqual(
            patron.nombre, retrieved_patron.nombre
        )  # Assert retrieved data matches

    def test_update_patron(self):
        """Tests updating an existing Patron"""
        patron = PatronFactory()
        patron.save()

        new_nombre = "Updated Company Name"
        patron.nombre = new_nombre
        patron.save()

        updated_patron = PatronModel.objects.get(pk=patron.pk)
        self.assertEqual(
            updated_patron.nombre, new_nombre
        )  # Assert update reflects in data

    def test_delete_patron(self):
        """Tests deleting an existing Patron"""
        patron = PatronFactory()
        patron.save()

        patron.delete()

        with self.assertRaises(PatronModel.DoesNotExist):
            PatronModel.objects.get(pk=patron.pk)  # Assert deletion using DoesNotExist


class ComentarioModelTest(TestCase):
    def test_create_comentario(self):
        """Tests creating a new Comentario"""
        patron = PatronFactory()
        comentario = ComentarioFactory(publicacion=patron)
        comentario.save()
        self.assertIsNotNone(comentario.pk)  # Assert that a primary key is assigned

    def test_read_comentario(self):
        """Tests retrieving an existing Comentario"""
        patron = PatronFactory()
        comentario = ComentarioFactory(publicacion=patron)
        comentario.save()

        retrieved_comentario = ComentarioModel.objects.get(pk=comentario.pk)
        self.assertEqual(
            comentario.comentario, retrieved_comentario.comentario
        )  # Assert data matches

    def test_update_comentario(self):
        """Tests updating an existing Comentario"""
        patron = PatronFactory()
        comentario = ComentarioFactory(publicacion=patron)
        comentario.save()

        new_comentario = "This is an updated comment"
        comentario.comentario = new_comentario
        comentario.save()

        updated_comentario = ComentarioModel.objects.get(pk=comentario.pk)
        self.assertEqual(
            updated_comentario.comentario, new_comentario
        )  # Assert update reflects

    def test_delete_comentario(self):
        """Tests deleting an existing Comentario"""
        patron = PatronFactory()
        comentario = ComentarioFactory(publicacion=patron)
        comentario.save()

        comentario.delete()

        with self.assertRaises(ComentarioModel.DoesNotExist):
            ComentarioModel.objects.get(
                pk=comentario.pk
            )  # Assert deletion using DoesNotExist


# Note: Tests for CotizacionModel and OrderModel would follow a similar structure
