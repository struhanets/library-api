from django.urls import path, include
from rest_framework import routers

from borrowings import views

router = routers.DefaultRouter()
router.register(r"borrowings", views.BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "borrowings"
