from django.db import models


class Books(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"

    title = models.CharField(max_length=150, unique=True)
    author = models.CharField(max_length=70)
    cover = models.CharField(max_length=50, choices=CoverChoices.choices)
    inventory = models.IntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
