from rest_framework import viewsets
from rest_framework.response import Response
from ..models import PhoneNumber
from ..serializers.s2_PhoneNumberSerializer import PhoneNumberSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from oauth2_provider.contrib.rest_framework import OAuth2Authentication


class PhoneNumberViewSet(viewsets.ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    format_kwarg = None
    permission_classes = [IsAdminUser]
    authentication_classes = [OAuth2Authentication]
