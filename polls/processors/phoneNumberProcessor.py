from ..models import PhoneNumber
from ..serializers.s2_PhoneNumberSerializer import PhoneNumberSerializer
from rest_framework.serializers import ValidationError


class PhoneNumberProcessor:

    def _verify_unique_phone_number(self, phone_number_data):

        phone_number_id = None

        phone_number = phone_number_data["number"]

        # Check if phone number exists
        phone_number_exists = PhoneNumber.objects.filter(number=phone_number).first()

        if phone_number_exists:
            # If an existing phone_number is found, set phone_number_id to its ID
            phone_number_id = phone_number_exists.id

            return phone_number_id

        else:

            try:

                phone_number_serializer = PhoneNumberSerializer(data=phone_number_data)
                # Check if the serializer is valid
                if phone_number_serializer.is_valid():
                    # Save the serializer instance
                    phone_number_serializer.save()
                    phone_number_id = phone_number_serializer.instance.id

                    return phone_number_id
                else:
                    # Raise a validation error if the serializer is not valid

                    raise ValidationError(
                        "Phone number creation failed:", phone_number_serializer.errors
                    )

            except ValidationError as e:
                raise e
