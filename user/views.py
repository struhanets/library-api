from django.contrib.auth import get_user_model
from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_object(self):
        return self.request.user
