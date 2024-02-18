from rest_framework import serializers
from ..models import Address
import re


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
        # Convert specific fields to uppercase before creating the object
        validated_data["street"] = validated_data.get("street", "").upper()
        validated_data["street_number"] = validated_data.get(
            "street_number", ""
        ).upper()
        validated_data["region_name"] = validated_data.get("region_name", "").upper()
        validated_data["prefecture_name"] = validated_data.get(
            "prefecture_name", ""
        ).upper()
        validated_data["postal_code"] = validated_data.get("postal_code", "").upper()

        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.street = validated_data.get("street", instance.street).upper()
        instance.street_number = validated_data.get(
            "street_number", instance.street_number
        ).upper()
        instance.region_name = validated_data.get("region_name", instance.region_name).upper()
        instance.prefecture_name = validated_data.get(
            "prefecture_name", instance.prefecture_name
        ).upper()
        instance.postal_code = validated_data.get("postal_code", instance.postal_code).upper()
        instance.save()
        return instance

    def validate_street(self, value):
        """
        Validate the street field.
        """
        return self.validate_address_field(value, "street")

    def validate_street_number(self, value):
        """
        Validate the street number field.
        """
        return self.validate_address_field(value, "street number")

    def validate_postal_code(self, value):
        """
        Validate the street number field.
        """
        return self.validate_address_field(value, "postal code")

    def validate_region_name(self, value):
        """
        Validate the region name field.
        """
        return self.validate_english_characters(value, "region name")

    def validate_prefecture_name(self, value):
        """
        Validate the prefecture name field.
        """
        return self.validate_english_characters(value, "prefecture name")

    def validate_address_field(self, value, field_name):
        """
        Validate an address field.
        """
        # Ensure that the value is not empty
        if not value:
            raise serializers.ValidationError(
                f"The {field_name} value cannot be empty."
            )

        # Validate the format using a regular expression
        if not re.match(r"^\d+[a-zA-Z]*$", value) or " " in value:
            raise serializers.ValidationError(
                f"The {field_name} must start with a number followed by none or more English letters and should not contain spaces."
            )

        # Ensure that the street number is a positive integer and not equal to 0
        if int(value[0]) <= 0:
            raise serializers.ValidationError(
                f"The {field_name} must be a positive integer and not equal to 0."
            )

        return value

    def validate_english_characters(self, value, field_name):
        """
        Validate that the value contains only English characters.
        """
        if not re.match(r"^[a-zA-Z\s]+$", value):
            raise serializers.ValidationError(
                f"The {field_name} must contain only English characters."
            )

        return value
