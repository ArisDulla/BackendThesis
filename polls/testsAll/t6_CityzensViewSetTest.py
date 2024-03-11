from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from ..viewsAll.v6_CityzensViewSet import CityzensViewSet
from ..models import CustomUser
from ..models import Address
from ..models import Cityzens
from ..models import PhoneNumber
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.test import force_authenticate


#
# python manage.py test polls.testsAll.t6_CityzensViewSetTest
#
class CityzensViewSetTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CityzensViewSet.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )
        self.retrieve_view = CityzensViewSet.as_view({"get": "retrieve"})

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
        # self.client.force_authenticate(user=self.admin_user)

        ######################################
        # CustomUser
        #
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

        customUser = CustomUser.objects.get(id=user.id)

        cityzens_data = {
            "user": customUser,
        }
        # create exist Citizen
        self.existsCityzens = Cityzens.objects.create(**cityzens_data)

        user = CustomUser.objects.create(
            username="testuser12321898",
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

        customUser = CustomUser.objects.get(id=user.id)

        cityzens_data = {
            "user": customUser,
        }
        # create exist Citizen
        self.existsCityzens22 = Cityzens.objects.create(**cityzens_data)

    # GET ALL phone_number
    def test_retrieve_all_phone_number(self):
        # Simulate GET request to retrieve all phoneNumber
        request = self.factory.get("/cityzens/")
        force_authenticate(request, user=self.admin_user)
        # force_authenticate(request, user=self.existsCityzens.user)

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # POST METHOD
    def test_create_user(self):

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
        cityzens_data = {
            "user": user_data,
        }

        request = self.factory.post("/cityzens/", cityzens_data, format="json")
        # force_authenticate(request, user=self.admin_user)

        response = self.view(request)
        response.render()

        # print("Response Content:", response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cityzens.objects.last().user.username, "testuser898213")

    # PUT METHOD
    def test_update_user(self):

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
        updated_cityzens_data = {
            "user": user_data,
        }

        request = self.factory.put(
            f"/cityzens/{self.existsCityzens.id}/", updated_cityzens_data, format="json"
        )

        force_authenticate(request, user=self.existsCityzens.user)
        # force_authenticate(request, user=self.existsCityzens22.user)
        # force_authenticate(request, user=self.admin_user)

        response = self.view(request, pk=self.existsCityzens.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.existsCityzens.refresh_from_db()

        self.assertEqual(self.existsCityzens.user.username, "arisdulla")
        self.assertEqual(self.existsCityzens.user.email, "it2194@hua.gr")
        self.assertEqual(self.existsCityzens.user.address.street, "ATHINAS13")
        self.assertEqual(self.existsCityzens.user.phone_number.number, "6988432143")

    # GET METHOD
    def test_retrieve_user(self):

        request = self.factory.get(f"/cityzens/")

        force_authenticate(request, user=self.existsCityzens.user)
        # force_authenticate(request, user=self.existsCityzens22.user)
        # force_authenticate(request, user=self.admin_user)

        response = self.retrieve_view(request, pk=self.existsCityzens.id)

        # Assert response status code and user retrieval
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # DELETE METHOD
    def test_delete_user(self):

        request = self.factory.delete(f"/cityzens/{self.existsCityzens.id}/")

        # force_authenticate(request, user=self.existsCityzens.user)
        # force_authenticate(request, user=self.existsCityzens22.user)
        force_authenticate(request, user=self.admin_user)

        response = self.view(request, pk=self.existsCityzens.id)

        # Assert response status code and user deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
