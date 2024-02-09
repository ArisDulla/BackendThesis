from rest_framework import serializers
from ..models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "street_number",
            "region_name",
            "prefecture_name",
            "postal_code",
        ]

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.street = validated_data.get("street", instance.street)
        instance.street_number = validated_data.get(
            "street_number", instance.street_number
        )
        instance.region_name = validated_data.get("region_name", instance.region_name)
        instance.prefecture_name = validated_data.get(
            "prefecture_name", instance.prefecture_name
        )
        instance.postal_code = validated_data.get("postal_code", instance.postal_code)
        instance.save()
        return instance
