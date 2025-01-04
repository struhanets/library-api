from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    BorrowingRetrieveSerializer,
    BorrowingReturnSerializer,
)

from borrowings.teleg_bot import send_telegram_message


@extend_schema(
    tags=["Borrowings"],
    description="Endpoints to manage borrowing option is library system. "
    "You can create and list data or filter by user_id and user_status parameters.",
)
class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def get_queryset(self):
        queryset = self.queryset

        user_id = self.request.query_params.get("user")
        user_status = self.request.query_params.get("user__is_active")

        if user_id:
            user_id = [int(str_id) for str_id in user_id.split(",")]
            queryset = queryset.filter(user_id__in=user_id)

        if user_status:
            if user_status.lower() in ["true", "1"]:
                user_status = True
            elif user_status.lower() in ["false", "0"]:
                user_status = False

            else:
                raise ValueError(
                    "Invalid value for user__is_active. Use 'true' or 'false'."
                )

            queryset = queryset.filter(user__is_active=user_status)

        return queryset

    def perform_create(self, serializer):
        borrowing = serializer.save()

        message = (
            "New borrowing create "
            f"user: {borrowing.user.first_name} {borrowing.user.last_name} "
            f"By books: {borrowing.book.title} "
            f"In date: {borrowing.borrow_date}"
        )

        send_telegram_message(message)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="user_id", type=int, description="filter by user_id"),
            OpenApiParameter(
                name="user_status",
                type=bool,
                description="filter by parameter user_is_active",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        List a queryset.
        """
        return super().list(request, *args, **kwargs)


@extend_schema(
    tags=["Borrowings"],
    description="Endpoints to manage the borrowing functionality in the library "
    "system allow you to update borrowing records, "
    "set the actual_return_date parameter, and return borrowed books to the inventory.",
)
class BorrowingsReturnView(generics.RetrieveUpdateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReturnSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        borrowing = serializer.save()

        if borrowing.actual_return_date:
            borrowing.book.inventory += 1
            borrowing.book.save()


class BorrowingsRetrieveView(generics.RetrieveUpdateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingRetrieveSerializer
    permission_classes = (IsAuthenticated,)
