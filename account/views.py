from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from . import serializer
from rest_framework import viewsets


# Create your views here.
# users/views.py
class UserView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = serializer.CreateUserSerializer




class UserDetailView(RetrieveAPIView):
    """
    用户详情
    """
    serializer_class = serializer.UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

