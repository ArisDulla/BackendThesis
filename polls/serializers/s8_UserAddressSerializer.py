from rest_framework import serializers
from ..models import UserAddress
from ..serializers.s1_AddressSerializer import AddressSerializer


class UserAddressSerializer(serializers.ModelSerializer):

    address = AddressSerializer()

    class Meta:
        model = UserAddress
        fields = [
            "id",
            "user",
            "address",
        ]
        read_only_fields = ["user"]

    def create(self, validated_data):

        address_data = validated_data.pop("address")

        address_serializer = AddressSerializer(data=address_data)

        if address_serializer.is_valid():
            address_instance = address_serializer.save()
        else:
            raise serializers.ValidationError(address_serializer.errors)

        addressUser_instance = UserAddress.objects.create(
            address=address_instance, **validated_data
        )

        return addressUser_instance

    def update(self, instance, validated_data):

        if "address" in validated_data:
            address_data = validated_data.pop("address")
            address_instance = instance.address

            address_serializer = AddressSerializer(
                address_instance, data=address_data, partial=True
            )
            if address_serializer.is_valid():
                address_instance = address_serializer.save()
            else:
                raise serializers.ValidationError(address_serializer.errors)

        instance.save()

        return instance
