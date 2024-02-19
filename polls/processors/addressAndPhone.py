from rest_framework.exceptions import ValidationError

from ..processors.addressProcessor import AddressProcessor
from ..processors.phoneNumberProcessor import PhoneNumberProcessor


class DepartmentCreationProcessor:
    def __init__(self):
        self.address_processor = AddressProcessor()
        self.phone_number_processor = PhoneNumberProcessor()

    def process_creation_data(self, request_data):
        # Process Address Data
        address_data = request_data["address"]
        try:
            address_id = self.address_processor._verify_unique_address(address_data)
        except ValidationError as e:
            raise e
        request_data["address"] = address_id

        # Process Phone Number Data
        phone_number_data = request_data["phone_number"]
        try:
            phone_number_id = self.phone_number_processor._verify_unique_phone_number(
                phone_number_data
            )
        except ValidationError as e:
            raise e
        request_data["phone_number"] = phone_number_id

        return request_data
