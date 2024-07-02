from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..models.User import User
from ..serializers.User import UserSerializer

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer