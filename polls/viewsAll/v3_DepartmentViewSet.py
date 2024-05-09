from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Department
from ..serializers.s3_DepartmentSerializer import DepartmentSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    format_kwarg = None
    permission_classes = [IsAdminUser]

    #
    # Override the update method
    #
    #  UPDATE - partial=True
    #
    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=200)

    #
    #
    # PUBLIC ACTION -- permission_classes = [ ]
    #
    @action(detail=True, methods=["get"], permission_classes=[])
    def get_specific_fields(self, request, pk=None):
        instance = self.get_object()
        data = {
            "name": instance.name,
            "email": instance.email,
            "street": instance.address.street if instance.address else None,
            "street_number": (
                instance.address.street_number if instance.address else None
            ),
            "region_name": instance.address.region_name if instance.address else None,
            "prefecture_name": (
                instance.address.prefecture_name if instance.address else None
            ),
            "postal_code": instance.address.postal_code if instance.address else None,
            "phone_number": (
                instance.phone_number.number if instance.phone_number else None
            ),
        }
        return Response(data)

    #
    #
    # PUBLIC ACTION -- permission_classes = [ ]
    #
    @action(detail=False, methods=["get"], permission_classes=[])
    def get_all(self, request):
        queryset = self.get_queryset()
        data = []
        for instance in queryset:
            user_data = {
                "id": instance.id,
                "name": instance.name,
                "email": instance.email,
                "street": instance.address.street if instance.address else None,
                "street_number": (
                    instance.address.street_number if instance.address else None
                ),
                "region_name": (
                    instance.address.region_name if instance.address else None
                ),
                "prefecture_name": (
                    instance.address.prefecture_name if instance.address else None
                ),
                "postal_code": (
                    instance.address.postal_code if instance.address else None
                ),
                "phone_number": (
                    instance.phone_number.number if instance.phone_number else None
                ),
            }
            data.append(user_data)
        return Response(data)
