from ..serializers.s4_CustomUserSerializer import CustomUserSerializer
from rest_framework.serializers import ValidationError


class CustomUserProcessor:

    def _create_custom_user(self, custom_user_data):

        try:
            serializer = CustomUserSerializer(data=custom_user_data)
            # Check if the serializer is valid
            if serializer.is_valid():
                # Save the serializer instance
                instance = serializer.save()

                custom_user_id = serializer.instance.id

                return {"user_id": custom_user_id, "instance": instance}

            else:
                # Raise a validation error if the serializer is not valid
                raise ValidationError("Custom user creation failed:", serializer.errors)

        except ValidationError as e:
            raise e

    def _update_custom_user(self, instance, custom_user_data):

        try:

            serializer = CustomUserSerializer(
                instance, data=custom_user_data, partial=True
            )

            # Check if the serializer is valid
            if serializer.is_valid():
                # Save the serializer instance
                serializer.save()
                return serializer.instance.id
            else:
                # Raise a validation error if the serializer is not valid
                raise ValidationError("Custom user update failed:", serializer.errors)

        except ValidationError as e:
            raise e
