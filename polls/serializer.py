from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        token["roleUser"] = _get_role_user(user)

        return token


class TokenStrategyMiddleware(MiddlewareMixin):

    @classmethod
    def obtain(cls, user):
        refresh = RefreshToken.for_user(user)

        refresh["roleUser"] = _get_role_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user,
        }


def _get_role_user(user):

    type_user = "NONE"
    #
    # FOR CITYZENS
    #
    if hasattr(user, "cityzens"):
        type_user = "cityzen"

    #
    # FOR Employee
    #
    elif hasattr(user, "employee"):
        employee = user.employee
        type = employee.employee_type

        if type == "YP01":
            type_user = "employeeYP01"

        elif type == "YP02":
            type_user = "employeeYP02"

        elif type == "SEC":
            type_user = "employeeSEC"

    #
    # FOR ADMIN
    #
    elif user.is_admin:
        type_user = "admin"

    return type_user
