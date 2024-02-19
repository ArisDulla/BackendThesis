from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from polls.models import Department, Address
from polls.viewsAll.v3_DepartmentViewSet import DepartmentViewSet
from django.urls import reverse
from rest_framework.test import APITestCase


class DepartmentViewSetTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DepartmentViewSet.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )
        self.address_data = {
            'street': '3MNBAAAAA',
            'street_number': '1',
            'region_name': 'RWWWW',
            'prefecture_name': 'RWWWW',
            'postal_code': '12345',
        }    