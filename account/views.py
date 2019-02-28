from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from . import serializer
from rest_framework.response import Response


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

    def get_serializer_class(self):
        if self.request.user.is_doctor is True:
            return serializer.DoctorDetailSerializer
        else:
            return serializer.UserDetailSerializer


class UserUpdateView(UpdateAPIView):
    """
    更新用户信息
    """

    serializer_class = serializer.UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ResetPasswordView(UpdateAPIView):
    serializer_class = serializer.ResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        data = {"detail": "Successful password change"}
        return Response(data)

    def get_object(self):
        return self.request.user


