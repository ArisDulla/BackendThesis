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

    #
    #  Retrieve department ID and citizen ID for the current user.
    #
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def get_department(self, request):

        user = request.user
        department_id = "NONE"
        user_id = "NONE"
        department_name = "NONE"
        type_user = "NONE"

        #
        #
        # FOR CITYZENS
        #
        if hasattr(user, "cityzens"):

            type_user = "cityzens"
            cityzen = user.cityzens

            department_id = cityzen.department_id

            user_id = cityzen.id

            if department_id:

                return Response(
                    {
                        "department_id": department_id,
                        "user_id": user_id,
                        "department_name": cityzen.department.name,
                        "type_user": type_user,
                    },
                    status=200,
                )
        #
        # FOR Employee
        #
        if hasattr(user, "employee"):

            employee = user.employee

            department_id = employee.department_id

            user_id = employee.id

            if department_id:
                return Response(
                    {
                        "department_id": department_id,
                        "user_id": user_id,
                        "department_name": employee.department.name,
                        "type_user": type_user,
                    },
                    status=200,
                )

        return Response(
            {
                "department_id": department_id,
                "user_id": user_id,
                "department_name": department_name,
                "type_user": type_user,
            },
            status=200,
        )

    #
    # Action get_role_user about -- Decide which dashboard to display in front based on the user's role --
    #
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def get_role_user(self, request):

        user = request.user
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

        return Response({"type_user": type_user}, status=200)
