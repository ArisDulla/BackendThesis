from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from ..viewsAll.v4_CustomUserViewSet import CustomUserViewSet
from ..models import CustomUser
from ..models import Address
from ..models import PhoneNumber
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.test import force_authenticate


#
# python manage.py test polls.testsAll.t4_CustomUserViewSetTest
#
class CustomUserViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CustomUserViewSet.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )
        self.retrieve_view = CustomUserViewSet.as_view({"get": "retrieve"})

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

        request = self.factory.post("/users/", self.user_data)
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.last().username, "testuser")

    # PUT METHOD
    def test_update_user(self):

        user = CustomUser.objects.create(
            username="existinguser",
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

        updated_user_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "password": "testpassword",
        }

        request = self.factory.put(f"/users/{user.id}/", updated_user_data)
        force_authenticate(request, user=self.admin_user)
        response = self.view(request, pk=user.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.username, "updateduser")

    def test_delete_custom_user(self):

        test_user = CustomUser.objects.create(
            username="existinguserew123123",
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
        # Simulate DELETE request to delete a custom user
        request = self.factory.delete(f"/users/{test_user.id}/")
        force_authenticate(request, user=self.admin_user)
        response = self.view(request, pk=test_user.id)

        # Assert response status code and user deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(id=test_user.id).exists())

    def test_list_custom_users(self):

        # Simulate GET request to list all custom users
        request = self.factory.get("/users/")
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)

        # Assert response status code and user list retrieval
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), CustomUser.objects.count())

    def test_retrieve_custom_user(self):

        test_user = CustomUser.objects.create(
            username="existinguserew123123",
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

        test_user_id = test_user.id
        request = self.factory.get(f"/users/")
        force_authenticate(request, user=self.admin_user)
        response = self.retrieve_view(request, pk=test_user_id)

        # Assert response status code and user retrieval
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], test_user.username)
