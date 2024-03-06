from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from ..viewsAll.v5_EmployeeViewSet import EmployeeViewSet
from ..models import CustomUser
from ..models import Address
from ..models import Employee
from ..models import PhoneNumber
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.test import force_authenticate
from ..models import Department


#
# python manage.py test polls.testsAll.t5_EmployeeViewSetTest
#
class EmployeeViewSetTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = EmployeeViewSet.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )

        self.address = Address.objects.create(
            street="456ElmSt",
            street_number="2",
            region_name="Region",
            prefecture_name="Prefecture",
            postal_code="54321",
        )

        self.phoneNumber = PhoneNumber.objects.create(
            number="6988433492",
            status="active",
        )

        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
            "date_joined": "2024-02-29T00:00:00Z",
            "last_login": "2024-02-29T00:00:00Z",
            "groups": [],
            "user_permissions": [],
            "address": self.address.id,
            "phone_number": self.phoneNumber.id,
        }

        self.address_instance = Address.objects.get(id=self.address.id)
        self.phone_number_instance = PhoneNumber.objects.get(id=self.phoneNumber.id)

        self.admin_user = get_user_model().objects.create_superuser(
            username="superuser", email="superuser@email.com", password="pass"
        )

        self.client = APIClient()  # Create APIClient instance
        self.client.force_authenticate(user=self.admin_user)

    # POST METHOD
    def test_create_user(self):

        ######################################
        # CustomUser
        user = CustomUser.objects.create(
            username="testuser898",
            password="testpassword",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            is_superuser=False,
            is_staff=False,
            is_active=True,
            date_joined="2024-02-29T00:00:00Z",
            last_login="2024-02-29T00:00:00Z",
            address=self.address_instance,
            phone_number=self.phone_number_instance,
        )
        ######################################

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

        user_data = {
            "username": "testuser898213",
            "password": "testpassword",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
            "date_joined": "2024-02-29T00:00:00Z",
            "last_login": "2024-02-29T00:00:00Z",
            "groups": [],
            "user_permissions": [],
            "address": address_data,
            "phone_number": number_data,
        }
        #
        # CREATE department
        #
        ###########################################

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

        ################################################

        employee_data = {
            "user": user_data,
            "department": departmentx.id,
            "employee_id": "1212",
            "employee_type": "YP02",
        }

        request = self.factory.post("/employees/", employee_data, format="json")
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.last().employee_id, "1212")

    # PUT METHOD
    def test_update_user(self):
        ######################################
        # CustomUser
        #
        # create existEmployee
        #
        user = CustomUser.objects.create(
            username="testuser898",
            password="testpassword",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            is_superuser=False,
            is_staff=False,
            is_active=True,
            date_joined="2024-02-29T00:00:00Z",
            last_login="2024-02-29T00:00:00Z",
            address=self.address_instance,
            phone_number=self.phone_number_instance,
        )

        address_data22 = {
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

        address = Address.objects.create(**address_data22)
        phoneNumber = PhoneNumber.objects.create(**number_data)

        department_data = {
            "name": "Test Department",
            "address": address,
            "phone_number": phoneNumber,
            "email": "test@example.com",
        }
        departmentx = Department.objects.create(**department_data)

        customUser = CustomUser.objects.get(id=user.id)
        department = Department.objects.get(id=departmentx.id)

        employee_data = {
            "user": customUser,
            "department": department,
            "employee_id": "1212",
            "employee_type": "YP02",
        }
        existsEmployee = Employee.objects.create(**employee_data)

        #
        # UPDATEDD DATA
        #
        # updated _user_data
        #
        #
        address_data = {
            "street": "athinas13",
            "street_number": "12",
            "region_name": "RWWWW",
            "prefecture_name": "RWWWW",
            "postal_code": "12345",
        }

        number_data = {
            "number": "6988432143",
            "status": "active",
        }

        user_data = {
            "username": "arisdulla",
            "password": "testpassword",
            "email": "it2194@hua.gr",
            "first_name": "Test",
            "last_name": "User",
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
            "date_joined": "2024-02-29T00:00:00Z",
            "last_login": "2024-02-29T00:00:00Z",
            "groups": [],
            "user_permissions": [],
            "address": address_data,
            "phone_number": number_data,
        }
        updated_user_data = {
            "user": user_data,
            "department": departmentx.id,
            "employee_id": "21311212",
            "employee_type": "YP02",
        }

        request = self.factory.put(
            f"/employees/{existsEmployee.id}/", updated_user_data, format="json"
        )

        force_authenticate(request, user=self.admin_user)

        response = self.view(request, pk=existsEmployee.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        existsEmployee.refresh_from_db()

        self.assertEqual(existsEmployee.user.username, "arisdulla")
        self.assertEqual(existsEmployee.user.email, "it2194@hua.gr")
        self.assertEqual(existsEmployee.user.address.street, "ATHINAS13")
        self.assertEqual(existsEmployee.user.phone_number.number, "6988432143")
