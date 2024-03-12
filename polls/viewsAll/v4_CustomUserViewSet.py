from rest_framework import viewsets
from ..models import CustomUser
from ..serializers.s4_CustomUserSerializer import CustomUserSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
