from ..models import Address
from ..serializers.s1_AddressSerializer import AddressSerializer
from rest_framework.serializers import ValidationError


class AddressProcessor:

    def _verify_unique_address(self, address_data):

        processed_address_data = {
            key: value.upper() if isinstance(value, str) else value
            for key, value in address_data.items()
        }

        address_id = None

        # Check if an address with the given data already exists
        existing_address = Address.objects.filter(**processed_address_data).first()

        if existing_address:
            # If an existing address is found, set address_id to its ID
            address_id = existing_address.id
            return address_id

        else:
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
