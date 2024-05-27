from rest_framework import viewsets
from ..models import CustomUser
from ..serializers.s4_CustomUserSerializer import CustomUserSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

    #
    # DJOSER endpoint to retrieve/update the authenticated user.
    # URL: /users/me/ ,GET, PUT and PATCH
    #
