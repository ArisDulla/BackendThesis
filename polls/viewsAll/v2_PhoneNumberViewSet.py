from ..serializers.s2_PhoneNumberSerializer import PhoneNumberSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from ..models import PhoneNumber


class PhoneNumberViewSet(viewsets.ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    permission_classes = [IsAdminUser]
