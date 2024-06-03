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
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination

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
    @action(detail=False, methods=["get"], permission_classes=[])
    def get_all(self, request):
        paginator = self.pagination_class()
        queryset = self.filter_queryset(self.get_queryset())
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
