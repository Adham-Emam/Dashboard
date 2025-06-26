from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views


urlpatterns = [
    path("", views.UserListView.as_view(), name="users-list"),
    path("register/", views.UserCreateView.as_view(), name="register"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    # JWT authentication endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # login
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # refresh
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
