from django.db import models
from django.db.models import CheckConstraint, Q, F

from books.models import Books


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField()
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(expected_return_date__gt=F("borrow_date"))
                | Q(actual_return_date__gt=F("borrow_date")),
                name="expected_return_date",
            ),
            CheckConstraint(
                condition=Q(actual_return_date__lte=F("expected_return_date")),
                name="correct_return_date",
            ),
        ]
