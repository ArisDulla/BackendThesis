from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        variables_array = _get_role_user(user)
        token["roleUser"] = variables_array["type_user"]
        token["department_name"] = variables_array["department_name"]
        token["department_id"] = variables_array["department_id"]
        token["user_Id_X"] = variables_array["user_id"]

        return token


class TokenStrategyMiddleware(MiddlewareMixin):

    @classmethod
    def obtain(cls, user):
        refresh = RefreshToken.for_user(user)

        variables_array = _get_role_user(user)
        refresh["roleUser"] = variables_array["type_user"]
        refresh["department_name"] = variables_array["department_name"]
        refresh["department_id"] = variables_array["department_id"]
        refresh["user_Id_X"] = variables_array["user_id"]

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user,
        }


class TokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            user_id = refresh["user_id"]
            User = get_user_model()
            user = User.objects.get(id=user_id)

            variables_array = _get_role_user(user)
            refresh["roleUser"] = variables_array["type_user"]
            refresh["department_name"] = variables_array["department_name"]
            refresh["department_id"] = variables_array["department_id"]
            refresh["user_Id_X"] = variables_array["user_id"]

            data["refresh"] = str(refresh)

        return data


def _get_role_user(user):

    type_user = "NONE"
    department_id = "NONE"
    department_name = "NONE"
    user_id = "NONE"

    variables_dict = {
        "type_user": "NONE",
        "department_id": "NONE",
        "department_name": "NONE",
        "user_id": "NONE",
    }

    #
    # FOR CITYZENS
    #
    if hasattr(user, "cityzens"):

        type_user = "cityzen"

        cityzen = user.cityzens
        user_id = cityzen.id

        if hasattr(cityzen, "department"):
            department_name = cityzen.department.name
            department_id = cityzen.department.id

    #
    # FOR Employee
    #
    elif hasattr(user, "employee"):

        employee = user.employee
        user_id = employee.id

        if hasattr(employee, "department"):
            department_name = employee.department.name
            department_id = employee.department.id

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

    variables_dict = {
        "type_user": type_user,
        "department_id": department_id,
        "department_name": department_name,
        "user_id": user_id,
    }

    return variables_dict
