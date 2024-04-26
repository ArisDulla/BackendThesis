from ..serializers.s2_PhoneNumberSerializer import PhoneNumberSerializer
from rest_framework.serializers import ValidationError


class PhoneNumberProcessor:

    def createPhoneNumber(self, phone_number_data):

        try:

            phone_number_serializer = PhoneNumberSerializer(data=phone_number_data)
            # Check if the serializer is valid
            if phone_number_serializer.is_valid():
                # Save the serializer instance
                phone_number_serializer.save()
                phone_number_id = phone_number_serializer.instance.id

                return phone_number_id
            else:

                raise ValidationError(
                    "Phone number creation failed:", phone_number_serializer.errors
                )

        except ValidationError as e:
            raise e
