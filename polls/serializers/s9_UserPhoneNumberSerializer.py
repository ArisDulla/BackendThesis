from rest_framework import serializers
from ..models import UserPhoneNumber
from ..serializers.s2_PhoneNumberSerializer import PhoneNumberSerializer


class UserPhoneNumberSerializer(serializers.ModelSerializer):

    phoneNumber = PhoneNumberSerializer()

    class Meta:
        model = UserPhoneNumber
        fields = [
            "id",
            "user",
            "phoneNumber",
        ]
        read_only_fields = ["user"]

    def create(self, validated_data):

        phoneNumber_data = validated_data.pop("phoneNumber")

        phoneNumber_serializer = PhoneNumberSerializer(data=phoneNumber_data)

        if phoneNumber_serializer.is_valid():
            phoneNumber_instance = phoneNumber_serializer.save()
        else:
            raise serializers.ValidationError(phoneNumber_serializer.errors)

        phoneNumberUser_instance = UserPhoneNumber.objects.create(
            phoneNumber=phoneNumber_instance, **validated_data
        )

        return phoneNumberUser_instance

    def update(self, instance, validated_data):

        if "phoneNumber" in validated_data:
            phoneNumber_data = validated_data.pop("phoneNumber")
            phoneNumber_instance = instance.phoneNumber

            phoneNumber_serializer = PhoneNumberSerializer(
                phoneNumber_instance, data=phoneNumber_data, partial=True
            )
            if phoneNumber_serializer.is_valid():
                phoneNumber_instance = phoneNumber_serializer.save()
            else:
                raise serializers.ValidationError(phoneNumber_serializer.errors)

        instance.save()

        return instance
