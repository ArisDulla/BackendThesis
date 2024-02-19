from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from polls.models import Department, Address, PhoneNumber
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
            "street": "3MNBAAAAA",
            "street_number": "1asd",
            "region_name": "RWWWW",
            "prefecture_name": "RWWWW",
            "postal_code": "12345",
        }
        self.number_data = {
            "number": "6988432143",
            "status": "active",
        }

    def test_create_department(self):

        # Create an address
        Address.objects.create(**self.address_data)
        PhoneNumber.objects.create(**self.number_data)

        address_data = {
            "street": "3MNBAAAAA",
            "street_number": "1",
            "region_name": "RWWWW",
            "prefecture_name": "RWWWW",
            "postal_code": "12345",
        }

        number_data = {
            "number": "6988432143",
            "status": "active",
        }

        # Department data 
        department_data = {
            "name": "Test Department",
            "address": address_data,
            "phone_number": number_data,
            "email": "test@example.com",
        }
        
        request = self.factory.post("/departments/", department_data, format="json")
        response = self.view(request)

        # Assert response status code and address creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.last().name, "Test Department")
        