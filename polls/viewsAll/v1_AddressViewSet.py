from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Address
from ..serializers.s1_AddressSerializer import AddressSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    format_kwarg = None
    permission_classes = [IsAdminUser]
