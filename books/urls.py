from django.urls import path, include
from rest_framework import routers

from books import views

router = routers.DefaultRouter()
router.register(r"books", views.BooksViewSet)

urlpatterns = [path("", include(router.urls))]


app_name = "books"
