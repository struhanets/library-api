from django.shortcuts import render
from rest_framework import viewsets

from books.models import Books
from books.serializers import BooksSerializer


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
