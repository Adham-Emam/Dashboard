from django.urls import path
from . import views


urlpatterns = [
    path("", views.ProductListCreateView.as_view(), name="product-list-create"),
    path("id/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path(
        "barcode/<str:barcode>/",
        views.ProductByBarcodeView.as_view(),
        name="product-by-barcode",
    ),
]
