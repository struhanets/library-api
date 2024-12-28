from rest_framework import serializers

from borrowings.models import Borrowing
from books.serializers import BooksSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = BooksSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )
        read_only_fields = (
            "id",
            "user",
        )
