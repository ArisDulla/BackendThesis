from rest_framework.exceptions import ValidationError

from ..processors.addressProcessor import AddressProcessor
from ..processors.phoneNumberProcessor import PhoneNumberProcessor
from ..serializers.s1_AddressSerializer import AddressSerializer
from ..serializers.s2_PhoneNumberSerializer import PhoneNumberSerializer


class AddressAndPhoneProcessor:
    def __init__(self):
        self.address_processor = AddressProcessor()
        self.phone_number_processor = PhoneNumberProcessor()

    def process_creation_data(self, request_data):
        #
        # Process Address Data
        #
        if "address" in request_data:

            if request_data["address"] != None:

                address_data = request_data["address"]
                try:
                    #
                    # CREATE ADDRESS
                    #
                    address_id = self.address_processor.create_address(address_data)
                except ValidationError as e:
                    raise e
                request_data["address"] = address_id

        if "phone_number" in request_data:
            # Process Phone Number Data

            if request_data["phone_number"] != None:

                phone_number_data = request_data["phone_number"]
                try:
                    #
                    # CREATE PHONE NUMBER
                    #
                    phone_number_id = self.phone_number_processor.createPhoneNumber(
                        phone_number_data
                    )
                except ValidationError as e:
                    raise e

                request_data["phone_number"] = phone_number_id

        return request_data

    def process_update_data(self, request_data, instance):
        #
        # UPDATE ADDRESS
        #
        if "address" in request_data:
            if request_data["address"] != None:

                address_data = request_data["address"]
                #
                # partial=True
                #
                serializer = AddressSerializer(
                    instance.address, data=address_data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

        #
        # UPDATE PHONE NUMBER
        #
        if "phone_number" in request_data:
            if request_data["phone_number"] != None:

                phone_number_data = request_data["phone_number"]

                #
                # partial=True
                #
                serializer = PhoneNumberSerializer(
                    instance.phone_number, data=phone_number_data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
