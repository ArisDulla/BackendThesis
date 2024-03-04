from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from polls.models import Department, Address, PhoneNumber
from polls.viewsAll.v3_DepartmentViewSet import DepartmentViewSet
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class DepartmentViewSetTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DepartmentViewSet.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )
        self.address_data = {
            "street": "3RWWWW",
            "street_number": "1",
            "region_name": "RWWWW",
            "prefecture_name": "RWWWWD",
            "postal_code": "12345",
        }
        self.number_data = {
            "number": "6988432143",
            "status": "active",
        }
        self.admin_user = get_user_model().objects.create_superuser(
            username="superuser", email="superuser@email.com", password="pass"
        )

        self.client = APIClient()  # Create APIClient instance
        self.client.force_authenticate(user=self.admin_user)

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
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)

        # Assert response status code and address creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.last().name, "Test Department")

    # PUT METHOD
    def test_update_department(self):

        address_data = {
            "street": "3RWWWWAA",
            "street_number": "1",
            "region_name": "RWWWW",
            "prefecture_name": "RWWWWD",
            "postal_code": "12345",
        }
        number_data = {
            "number": "6988432999",
            "status": "active",
        }
        # Create an address
        address = Address.objects.create(**address_data)
        phoneNumber = PhoneNumber.objects.create(**number_data)

        department_data = {
            "name": "Test Department",
            "address": address,
            "phone_number": phoneNumber,
            "email": "test@example.com",
        }
        departmentx = Department.objects.create(**department_data)

        address_data = {
            "street": "3RWWWWAA",
            "street_number": "1",
            "region_name": "RWWWW",
            "prefecture_name": "RWWWWD",
            "postal_code": "12345",
        }

        number_data = {
            "number": "6988432999",
            "status": "active",
        }

        updated_department_data = {
            "name": "Test",
            "address": address_data,
            "phone_number": number_data,
            "email": "test@example.com",
        }

        request = self.factory.put(
            f"/phoneNumber/{departmentx.id}/", updated_department_data, format="json"
        )
        force_authenticate(request, user=self.admin_user)
        response = self.view(request, pk=departmentx.id)

        # Assert response status code and address update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        departmentx.refresh_from_db()
        self.assertEqual(departmentx.name, "Test")
