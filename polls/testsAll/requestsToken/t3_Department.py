import requests
import unittest
from decouple import config


#
#  python manage.py test polls.testsAll.requestsToken.t3_Department
#
class TestDepartmentAPI(unittest.TestCase):
    def test_post_department(self):

        auth_token = config("TEST_AUTH_TOKEN")

        # Define headers
        headers = {"Authorization": auth_token}

        # Define JSON data
        data = {
            "name": "asdsaadssdaas",
            "address": {
                "street": "3MNBAAAAA",
                "street_number": "1",
                "region_name": "RWWWW",
                "prefecture_name": "RWWWW",
                "postal_code": "12345",
            },
            "phone_number": {"number": "6988432143", "status": "active"},
            "email": "test@example.com",
        }
        # Make the POST request
        response = requests.post(
            "http://127.0.0.1:8000/api/departments/", headers=headers, json=data
        )

        # Assert response status code
        self.assertEqual(response.status_code, 201)
