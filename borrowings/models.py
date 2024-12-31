from django.db import models
from django.db.models import CheckConstraint, Q, F

from books.models import Books
from city_library_project.settings import AUTH_USER_MODEL


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer"
    )

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(actual_return_date__gt=F("borrow_date")) & Q(expected_return_date__gt=F("borrow_date")),
                name="correct_return_date",
            ),
        ]
