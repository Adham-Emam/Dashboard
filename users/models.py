from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Authentication fields
    username = None
    email = models.EmailField(
        unique=True,
        error_messages={"unique": "This email is already registered."},
    )

    # User details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
