from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Inventory
from products.models import Product

User = get_user_model()


class InventoryAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass123"
        )

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=9.99,
            barcode="1234567890123",
        )

        self.product_data = {
            "id": 2,
            "name": "New Product",
            "description": "New Description",
            "category": "Electronics",
            "brand_name": "BrandX",
            "price": 19.99,
            "barcode": "0987654321123",
        }

        # Create sample inventory item
        self.inventory = Inventory.objects.create(product=self.product, quantity=10)

        # URLs
        self.list_url = reverse("inventory-list")  # Update with your actual URL name
        self.detail_url = reverse(
            "inventory-detail", kwargs={"pk": self.inventory.pk}
        )  # Update with your URL name

        # Authenticate and store access token
        token_url = reverse("token_obtain_pair")
        response = self.client.post(
            token_url,
            {"email": "testuser@example.com", "password": "testpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_inventory_list_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_inventory_list_authenticated(self):
        self.authenticate()
        response = self.client.get(self.list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_inventory_unauthenticated(self):
        data = {"product": self.product.id, "quantity": 5, "location": "Warehouse A"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_inventory_authenticated(self):
        self.authenticate()
        data = {"product": self.product.id, "quantity": 5, "location": "Warehouse A"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["product_name"], "Test Product")

    def test_retrieve_inventory(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product_name"], self.inventory.product.name)

    def test_update_inventory_authenticated(self):
        self.authenticate()
        data = {
            "quantity": 15,
        }
        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], 15)

    def test_update_inventory_unauthenticated(self):
        data = {
            "quantity": 5,
        }
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_inventory_authenticated(self):
        self.authenticate()
        response = self.client.delete(self.detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Inventory.objects.filter(pk=self.inventory.pk).exists())

    def test_delete_inventory_unauthenticated(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
