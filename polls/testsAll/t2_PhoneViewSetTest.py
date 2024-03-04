from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from polls.models import PhoneNumber
from polls.viewsAll.v2_PhoneNumberViewSet import PhoneNumberViewSet
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

# run test  python manage.py test polls.testsAll.PhoneViewSetTest
class PhoneNumberViewSetTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PhoneNumberViewSet.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )
        self.retrieve_view = PhoneNumberViewSet.as_view({"get": "retrieve"})

        self.phone_number_data = {
            "number": "6988433421",
            "status": "active",
        }
        
        self.admin_user = get_user_model().objects.create_superuser(
            username="superuser", email="superuser@email.com", password="pass"
        )

        self.client = APIClient()  # Create APIClient instance
        self.client.force_authenticate(user=self.admin_user)

    # POST METHOD
    def test_create_phone_number(self):

        # Simulate POST request to create an phone_number
        request = self.factory.post("/phoneNumber/", self.phone_number_data)
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)

        # Assert response status code and phone_number creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PhoneNumber.objects.last().number, "6988433421")

    # PUT METHOD
    def test_update_phone_number(self):
        phoneNumber = PhoneNumber.objects.create(
            number="6988433492",
            status="active",
        )

        updated_phoneNumber_data = {
            "number": "6988477777",
            "status": "not_exist",
        }

        request = self.factory.put(
            f"/phoneNumber/{phoneNumber.id}/", updated_phoneNumber_data
        )
        force_authenticate(request, user=self.admin_user)
        response = self.view(request, pk=phoneNumber.id)

        # Assert response status code and phoneNumber update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        phoneNumber.refresh_from_db()
        self.assertEqual(phoneNumber.number, "6988477777")

    # DELETE METHOD
    def test_delete_phone_number(self):
        # Create an phone_number
        phoneNumber = PhoneNumber.objects.create(
            number="6988433492",
            status="active",
        )

        # Simulate DELETE request to delete the phoneNumber
        request = self.factory.delete(f"/phoneNumber/{phoneNumber.id}/")
        force_authenticate(request, user=self.admin_user)
        response = self.view(request, pk=phoneNumber.id)

        # Assert response status code and phoneNumber deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PhoneNumber.objects.filter(id=phoneNumber.id).exists())

    # GET 1 phone_number
    def test_retrieve_phone_number(self):
        # Create an phone_number
        phoneNumber = PhoneNumber.objects.create(
            number="6988433492",
            status="active",
        )

        # Simulate GET request to retrieve the phoneNumber
        request = self.factory.get(f"/phoneNumber/{phoneNumber.id}/")
        force_authenticate(request, user=self.admin_user)
        response = self.retrieve_view(request, pk=phoneNumber.id)

        # Assert response status code and phoneNumber retrieval
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number"], "6988433492")

    # GET ALL phone_number
    def test_retrieve_all_phone_number(self):
        # Create some phone_number
        phoneNumber_data = [
            {
                "number": "6988477777",
                "status": "active",
            },
            {
                "number": "6988477774",
                "status": "active",
            },
        ]

        # Simulate POST requests to create phoneNumber
        for data in phoneNumber_data:
            request = self.factory.post("/phoneNumber/", data)
            force_authenticate(request, user=self.admin_user)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Simulate GET request to retrieve all phoneNumber
        request = self.factory.get("/phoneNumber/")
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)

        # Assert response status code and phoneNumber retrieval
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        phoneNumber = response.data
        print("Retrieved phoneNumber:")
        for phone in phoneNumber:
            print(phone)

        self.assertEqual(len(response.data), 2)
