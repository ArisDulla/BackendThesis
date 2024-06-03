from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Department
from ..serializers.s3_DepartmentSerializer import DepartmentSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    format_kwarg = None
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ["list", "get_all"]:
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

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
    @action(detail=False, methods=["get"])
    def get_all(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
