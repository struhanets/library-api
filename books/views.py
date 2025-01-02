from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from books.models import Books
from books.serializers import BooksSerializer


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (IsAdminUser,)

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return (IsAdminUser(),)
