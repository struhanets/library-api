from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics

from user.serializers import UserSerializer


@extend_schema(
    tags=["User"], description="You can create a new user using this endpoint."
)
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


@extend_schema(
    tags=["User"],
    description="Endpoints for managing user information allow you to view and update records for the current user.",
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_object(self):
        return self.request.user
