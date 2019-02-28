from django.urls import path
from .views import UserView, UserDetailView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('create/', UserView.as_view()),
    path('detail/', UserDetailView.as_view()),
    path('authorizations/', obtain_jwt_token, name='authorizations'),
]
