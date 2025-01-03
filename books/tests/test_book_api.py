from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from books.models import Books
from books.serializers import BooksSerializer

BASE_URL = reverse("books:books-list")


def detail_url(book_id):
    return reverse("books:books-detail", args=[book_id])


def sample_book(**params) -> Books:
    default = {
        "title": "Sample Title",
        "author": "Sample Author",
        "cover": "SOFT",
        "inventory": 15,
        "daily_fee": 15.40,
    }
    default.update(params)
    return Books.objects.create(**default)


class UnauthenticatedTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_get(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_post(self):
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_retrieve_detail(self):
        book = sample_book()
        response = self.client.get(detail_url(book.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthenticatedTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test12345",
        )

        self.client.force_authenticate(self.user)

    def test_authenticated_list(self):
        sample_book()

        response = self.client.get(BASE_URL)
        buses = Books.objects.all()
        serializer = BooksSerializer(buses, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_books_detail(self):
        book = sample_book()
        response = self.client.get(detail_url(book.id))

        serializer = BooksSerializer(book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_forbidden(self):
        payload = {
            "title": "Sample Title",
            "author": "Sample Author",
            "cover": "SOFT",
            "inventory": 15,
            "daily_fee": 15.40,
        }

        response = self.client.post(BASE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminBooksTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.com", password="admin12345", is_staff=True
        )

        self.client.force_authenticate(self.user)

    def test_book_create(self):
        payload = {
            "title": "Sample Title",
            "author": "Sample Author",
            "cover": "SOFT",
            "inventory": 15,
            "daily_fee": 15.40,
        }

        response = self.client.post(BASE_URL, payload)

        book = Books.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            if key in ["title", "author"]:
                self.assertEqual((payload[key]), getattr(book, key))
