from rest_framework import serializers
from ..models import Department
from ..serializers.s1_AddressSerializer import AddressSerializer
from ..serializers.s2_PhoneNumberSerializer import PhoneNumberSerializer
from django.db import transaction


class DepartmentSerializer(serializers.ModelSerializer):

    address = AddressSerializer()
    phone_number = PhoneNumberSerializer()

    class Meta:
        model = Department
        fields = ["id", "name", "address", "phone_number", "email"]

        def validate_email(self, value):
            if "@" not in value or "." not in value:
                raise serializers.ValidationError(
                    "Invalid email address. Must contain '@' and '.'"
                )
            return value

    def create(self, validated_data):

        with transaction.atomic():
            #
            #  Address Data
            #
            address_data = validated_data.pop("address")

            address_serializer = AddressSerializer(data=address_data)
            if address_serializer.is_valid():
                address_instance = address_serializer.save()
            else:
                raise serializers.ValidationError(address_serializer.errors)

            #
            #  Phone Number Data
            #
            phone_number_data = validated_data.pop("phone_number")

            phone_number_serializer = PhoneNumberSerializer(data=phone_number_data)
            if phone_number_serializer.is_valid():
                phone_number_instance = phone_number_serializer.save()
            else:
                raise serializers.ValidationError(phone_number_serializer.errors)

            #
            # Department Data
            #
            employee_instance = Department.objects.create(
                phone_number=phone_number_instance,
                address=address_instance,
                **validated_data
            )
            return employee_instance

    def update(self, instance, validated_data):
        #
        #  Address Data
        #
        if "address" in validated_data:
            address_data = validated_data.pop("address")
            address_instance = instance.address

            if address_instance is None:
                address_serializer = AddressSerializer(data=address_data)

            else:
                address_serializer = AddressSerializer(
                    address_instance, data=address_data, partial=True
                )

            if address_serializer.is_valid():
                instance.address = address_serializer.save()
            else:
                raise serializers.ValidationError(address_serializer.errors)

        #
        # Phone Number Data
        #
        if "phone_number" in validated_data:
            phone_number_data = validated_data.pop("phone_number")
            phone_number_instance = instance.phone_number

            if phone_number_instance is None:
                phone_number_serializer = PhoneNumberSerializer(data=phone_number_data)

            else:
                phone_number_serializer = PhoneNumberSerializer(
                    phone_number_instance, data=phone_number_data, partial=True
                )

            if phone_number_serializer.is_valid():
                instance.phone_number = phone_number_serializer.save()
            else:
                raise serializers.ValidationError(phone_number_serializer.errors)

        #
        # Department Data
        #
        instance.email = validated_data.get("email", instance.email)
        instance.name = validated_data.get("name", instance.name)

        instance.save()

        return instance
