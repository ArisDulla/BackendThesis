from ..serializers.s4_CustomUserSerializer import CustomUserSerializer
from rest_framework.serializers import ValidationError
from ..models import CustomUser
from rest_framework.authtoken.models import Token


class CustomUserProcessor:

    def _create_custom_user(self, custom_user_data):

        try:

            serializer = CustomUserSerializer(data=custom_user_data)
            # Check if the serializer is valid
            if serializer.is_valid():
                # Save the serializer instance
                serializer.save()

                custom_user_id = serializer.instance.id

                user = serializer.instance
                token, created = Token.objects.get_or_create(user=user)

                return {"token": token.key, "user_id": custom_user_id}

            else:
                # Raise a validation error if the serializer is not valid
                raise ValidationError("Custom user creation failed:", serializer.errors)

        except ValidationError as e:
            raise e

    def _update_custom_user(self, instance, custom_user_data):

        try:

            serializer = CustomUserSerializer(instance, data=custom_user_data)

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
