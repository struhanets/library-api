from django.urls import path, include

from borrowings import views
from borrowings.views import (
    BorrowingViewSet,
    BorrowingsRetrieveView,
    BorrowingsReturnView,
)

borrowings_list = BorrowingViewSet.as_view(actions={"get": "list", "post": "create"})

urlpatterns = [
    path("borrowings/", borrowings_list, name="borrowings-list"),
    path(
        "borrowings/<int:pk>/",
        BorrowingsRetrieveView.as_view(),
        name="borrowings-detail",
    ),
    path(
        "borrowings/<int:pk>/return/",
        BorrowingsReturnView.as_view(),
        name="borrowings-return",
    ),
]

app_name = "borrowings"
