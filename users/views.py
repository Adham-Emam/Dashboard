from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import CustomUserSerializer, CustomUserCreateSerializer
from .models import CustomUser


class UserListView(generics.ListAPIView):
    """
    View to list all users.
    Accessible only to staff members.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserCreateView(generics.CreateAPIView):
    """
    View to create a new user.
    Accessible to any authenticated user.
    """

    serializer_class = CustomUserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                CustomUserSerializer(user).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a user.
    Accessible only to staff members.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]
