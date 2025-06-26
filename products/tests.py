from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()


class ProductAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass123"
        )
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=9.99,
            barcode="1234567890",
        )
        self.list_url = reverse("product-list-create")
        self.detail_url = reverse("product-detail", kwargs={"pk": self.product.pk})
        self.barcode_url = reverse(
            "product-by-barcode", kwargs={"barcode": self.product.barcode}
        )
        self.product_data = {
            "name": "New Product",
            "description": "New Description",
            "category": "Electronics",
            "brand_name": "BrandX",
            "price": 19.99,
            "barcode": "0987654321",
        }

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

    def test_list_products(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_authenticated(self):
        self.authenticate()
        response = self.client.post(self.list_url, self.product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_unauthenticated(self):
        response = self.client.post(self.list_url, self.product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_product_by_id(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product_by_barcode(self):
        response = self.client.get(self.barcode_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_authenticated(self):
        self.authenticate()
        response = self.client.patch(
            self.detail_url,
            {
                "name": "Updated Product",
                "description": "Updated",
                "price": 12.34,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_unauthenticated(self):
        response = self.client.patch(
            self.detail_url,
            {
                "name": "Updated Product",
                "description": "Updated",
                "price": 12.34,
                "barcode": self.product.barcode,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_product_authenticated(self):
        self.authenticate()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_unauthenticated(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
