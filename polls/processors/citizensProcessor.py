from ..models import Cityzens
from ..serializers.s6_CityzensSerializer import CityzensSerializer
from rest_framework.serializers import ValidationError


class CitizensProcessor:

    def _cityzens_exists(self, userId):
        return Cityzens.objects.filter(user=userId).exists()

    def _create_cityzen(self, userId):

        cityzens_data = {
            "user": userId,
        }

        try:

            serializer = CityzensSerializer(data=cityzens_data)
            # Check if the serializer is valid
            if serializer.is_valid():
                # Save the serializer instance
                serializer.save()

            else:
                # Raise a validation error if the serializer is not valid
                raise ValidationError(
                    "Custom user creation failed:",
                    serializer.errors,
                )

        except ValidationError as e:
            raise
