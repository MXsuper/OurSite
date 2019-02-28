from django.urls import path, include
from .views import UserView, UserDetailView, UserUpdateView, ResetPasswordView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('create/', UserView.as_view()),
    path('detail/', UserDetailView.as_view()),
    path('update/', UserUpdateView.as_view()),
    path('reset_password/', ResetPasswordView.as_view()),
    path('authorizations/', obtain_jwt_token, name='authorizations'),
]
