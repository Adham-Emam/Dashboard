from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser


class UserTests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
        )

        self.normal_user = CustomUser.objects.create_user(
            email="user@example.com",
            password="userpass",
            first_name="Normal",
            last_name="User",
        )

    def test_user_registration(self):

        url = reverse("register")
        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "newpass123",
        }

        # Login as existing user to access registration endpoint
        self.client.login(email="user@example.com", password="userpass")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 3)
        self.assertEqual(CustomUser.objects.latest("id").email, "newuser@example.com")

    def test_jwt_login(self):
        url = reverse("token_obtain_pair")
        data = {"email": "user@example.com", "password": "userpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_jwt_access_protected_route(self):
        url = reverse("users-list")

        # Get token
        token_response = self.client.post(
            reverse("token_obtain_pair"),
            {"email": "admin@example.com", "password": "adminpass"},
            format="json",
        )
        access_token = token_response.data["access"]

        # Set Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_cannot_access_user_list(self):
        token_response = self.client.post(
            reverse("token_obtain_pair"),
            {"email": "user@example.com", "password": "userpass"},
            format="json",
        )
        access_token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
