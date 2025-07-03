from rest_framework import viewsets, permissions
from .models import Transaction, TransactionItem
from .serializers import TransactionSerializer, TransactionItemSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(performed_by=self.request.user)
