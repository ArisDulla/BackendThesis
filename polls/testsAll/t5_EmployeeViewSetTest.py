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

        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test324234452@example.com",
            "first_name": "Test",
            "last_name": "User",
            "is_superuser": False,
            "is_active": True,
            "last_login": "2024-02-29T00:00:00Z",
            "groups": [],
            "user_permissions": [],
        }

        self.admin_user = get_user_model().objects.create_superuser(
            username="superuser",
            email="superuser5v4353@email.com",
            password="pass",
            first_name= "Test",
            last_name= "User",
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
            email="test623423@example.com",
            first_name="Test",
            last_name="User",
            is_superuser=False,
            is_active=True,
            last_login="2024-02-29T00:00:00Z",
        )

        user_data = {
            "username": "testuser898213",
            "password": "testpassword",
            "email": "test123123123@example.com",
            "first_name": "Test",
            "last_name": "User",
            "is_superuser": False,
            "is_active": True,
            "last_login": "2024-02-29T00:00:00Z",
            "groups": [],
            "user_permissions": [],
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
            "email": "test435213134@example.com",
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

        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(Employee.objects.last().employee_id, "1212")

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
            email="test5423214@example.com",
            first_name="Test",
            last_name="User",
            is_superuser=False,
            is_active=True,
            last_login="2024-02-29T00:00:00Z",
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
            "email": "test6232452@example.com",
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

        user_data = {
            "username": "arisdulla",
            "password": "testpassword",
            "email": "it219423423442@hua.gr",
            "first_name": "Test",
            "last_name": "User",
            "is_superuser": False,
            "is_active": True,
            "last_login": "2024-02-29T00:00:00Z",
            "groups": [],
            "user_permissions": [],
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
        self.assertEqual(existsEmployee.user.email, "it219423423442@hua.gr")
