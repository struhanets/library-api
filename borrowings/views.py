from rest_framework import viewsets, generics

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    BorrowingRetrieveSerializer,
)

from borrowings.teleg_bot import send_telegram_message


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

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
            "New borrowing create ",
            f"user: {borrowing.user.first_name} {borrowing.user.last_name} ",
            f"By books: {borrowing.book.title}" f"In date: {borrowing.borrow_date}",
        )

        send_telegram_message(message)


class BorrowingsRetrieveView(generics.RetrieveUpdateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingRetrieveSerializer

    def perform_update(self, serializer):
        borrowing = serializer.save()

        if borrowing.actual_return_date:
            borrowing.book.inventory += 1
            borrowing.book.save()
