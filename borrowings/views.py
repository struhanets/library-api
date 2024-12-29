from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingCreateSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticatedOrReadOnly]
        return [permissions.IsAdminUser]
