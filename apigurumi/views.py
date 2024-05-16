from rest_framework import generics, permissions
from amigurumi.models import PatronModel
from .serializers import PatronSerializer


class PatronListApi(generics.ListAPIView):
    """API view for retrieving a list of PatronModel objects."""

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]  # Adjust permissions as required
    queryset = PatronModel.objects.all()  # Fetch all Patron objects
    serializer_class = PatronSerializer
