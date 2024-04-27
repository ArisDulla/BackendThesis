from rest_framework import serializers
from ..models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        ]
        read_only_fields = ["is_superuser", "is_staff", "is_active"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """
        Override the create method to use CustomUserManager's create_user method.
        """
        user = CustomUser.objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):

        if "password" in validated_data:

            instance.set_password(validated_data["password"])

            del validated_data["password"]

        return super().update(instance, validated_data)
