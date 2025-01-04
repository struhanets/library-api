from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from books.models import Books
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingCreateSerializer

BORROWINGS_URL = reverse("borrowings:borrowings-list")


def return_url(borrowing_id):
    return reverse("borrowings:borrowings-return", args=[borrowing_id])


class UnauthenticatedTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_get(self):
        response = self.client.get(BORROWINGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_post(self):
        response = self.client.post(BORROWINGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="test12345"
        )

        self.client.force_authenticate(self.user)

        self.book = Books.objects.create(
            title="test1", author="test", cover="HARD", inventory=10, daily_fee=14.50
        )

    def test_authenticated_get(self):
        borrowing = Borrowing.objects.create(
            expected_return_date="2025-01-15",
            user=self.user,
            book=self.book,
        )

        response = self.client.get(BORROWINGS_URL)

        borrowings = Borrowing.objects.all()
        serializer = BorrowingSerializer(borrowings, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_borrowing_create_and_decrease_book_inventory(self):
        inventory = self.book.inventory

        payload = {
            "expected_return_date": "2025-01-15",
            "book": self.book.title,
            "user": self.user.id,
        }

        response = self.client.post(BORROWINGS_URL, payload)

        borrowing = Borrowing.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, inventory - 1)

        for key in payload:
            if key == "expected_return_date":
                self.assertEqual(payload[key], response.data["expected_return_date"])
            if key == "book":
                self.assertEqual(payload[key], borrowing.book.title)
            if key == "user":
                self.assertEqual(payload[key], borrowing.user.id)

    def test_update_borrowing_details_and_increase_book_inventory(self):

        borrowing = Borrowing.objects.create(
            expected_return_date="2025-01-15",
            user=self.user,
            book=self.book,
        )
