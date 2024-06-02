from ..serializers.s1_AddressSerializer import AddressSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from ..models import Address


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAdminUser]
