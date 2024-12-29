from rest_framework import serializers

from books.models import Books
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
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


class BorrowingCreateSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(
        slug_field="title", queryset=Books.objects.all()
    )

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

    def create(self, validated_data):
        book = validated_data["book"]

        # Перевіряємо наявність книг в інвентарі
        if book.inventory <= 0:
            raise serializers.ValidationError("No books available in the inventory.")

        # Зменшуємо інвентар на 1
        book.inventory -= 1
        book.save()  # Зберігаємо зміни в інвентарі

        borrowing = Borrowing.objects.create(**validated_data)

        return borrowing
