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
