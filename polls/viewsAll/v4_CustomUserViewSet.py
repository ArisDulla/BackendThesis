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
        cityzen_id = "NONE"
        #
        #
        # FOR CITYZENS
        #
        if hasattr(user, "cityzens"):
            cityzen = user.cityzens

            department_id = user.cityzens.department_id

            cityzen_id = user.cityzens.id

            if department_id:
                return Response(
                    {"department_id": department_id, "cityzen_id": cityzen_id},
                    status=200,
                )

        # User does not have a cityzen profile
        return Response(
            {"department_id": department_id, "cityzen_id": cityzen_id}, status=200
        )
