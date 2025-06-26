from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Inventory
from .serializers import InventorySerializer


class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "product_name"

    def get(self, request, *args, **kwargs):
        inventories = self.get_queryset()
        serializer = self.get_serializer(inventories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        inventory = self.get_object()
        serializer = self.get_serializer(inventory)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        inventory = self.get_object()
        serializer = self.get_serializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        inventory = self.get_object()
        inventory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
