import requests
import unittest
from decouple import config


#
# python manage.py test polls.testsAll.requestsToken.t5_Employee
#
class TestEmployeeAPI(unittest.TestCase):
    def test_post_employee(self):

        auth_token = config("TEST_AUTH_TOKEN")

        # Define headers
        headers = {"Authorization": auth_token}

        # Define JSON data
        data = {
            "user": {
                "username": "teassaasdsdsasda213",
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
                "address": {
                    "street": "3MNBAAAAA",
                    "street_number": "1",
                    "region_name": "RWWWW",
                    "prefecture_name": "RWWWW",
                    "postal_code": "12345",
                },
                "phone_number": {"number": "6988432143", "status": "active"},
            },
            "department": 1,
            "employee_id": "1212",
            "employee_type": "YP02",
        }

        # Make the POST request
        response = requests.post(
            "http://127.0.0.1:8000/api/employees/", headers=headers, json=data
        )

        # Assert response status code
        self.assertEqual(response.status_code, 201)
