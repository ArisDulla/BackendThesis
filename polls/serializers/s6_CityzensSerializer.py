from rest_framework import serializers
from ..models import Cityzens


class CityzensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cityzens
        fields = ["id", "user"]
