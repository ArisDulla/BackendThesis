from ..serializers.s1_AddressSerializer import AddressSerializer
from rest_framework.serializers import ValidationError


class AddressProcessor:

    def create_address(self, address_data):

        try:

            address_serializer = AddressSerializer(data=address_data)
            # Check if the serializer is valid
            if address_serializer.is_valid():
                # Save the serializer instance
                address_serializer.save()

                address_id = address_serializer.instance.id

                return address_id
            else:
                # Raise a validation error if the serializer is not valid

                raise ValidationError(
                    "Address creation failed:", address_serializer.errors
                )

        except ValidationError as e:
            raise e
