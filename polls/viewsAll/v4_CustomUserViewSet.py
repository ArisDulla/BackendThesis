from rest_framework import viewsets
from ..models import CustomUser
from ..serializers.s4_CustomUserSerializer import CustomUserSerializer
from rest_framework.permissions import IsAdminUser
from oauth2_provider.contrib.rest_framework import OAuth2Authentication


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [OAuth2Authentication]
