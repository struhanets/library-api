from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from books.models import Books
from books.serializers import BooksSerializer


@extend_schema(
    tags=["Books"],
    description="Endpoints to manage books in the library"
    "You can create, list, retrieve, update, or delete books",
)
class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (IsAdminUser,)

    def get_permissions(self):
        if self.action in (
            "list",
            "retrieve",
        ):
            return (AllowAny(),)
        return (IsAdminUser(),)
