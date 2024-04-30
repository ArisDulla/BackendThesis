from rest_framework import serializers
from ..models import Cityzens
from ..serializers.s4_CustomUserSerializer import CustomUserSerializer
from django.db import transaction


class CityzensSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Cityzens
        fields = ["id", "user", "department"]
        read_only_fields = ["department"]

    def create(self, validated_data):

        with transaction.atomic():
            user_data = validated_data.pop("user")

            user_serializer = CustomUserSerializer(data=user_data)
            if user_serializer.is_valid():
                user_instance = user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)

            employee_instance = Cityzens.objects.create(
                user=user_instance, **validated_data
            )
            return employee_instance

    def update(self, instance, validated_data):

        if "user" in validated_data:
            user_data = validated_data.pop("user")
            user_instance = instance.user

            user_serializer = CustomUserSerializer(
                user_instance, data=user_data, partial=True
            )
            if user_serializer.is_valid():
                user_instance = user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)

        instance.department = validated_data.get("department", instance.department)
        instance.save()

        return instance
