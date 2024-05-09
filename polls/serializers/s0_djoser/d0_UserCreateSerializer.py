from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "username")

    def update(self, instance, validated_data):

        if "password" in validated_data:

            instance.set_password(validated_data["password"])

            del validated_data["password"]

        return super().update(instance, validated_data)

    """
    #
    # CREATE +NEW CITYZEN ( Override the perform_create method )
    #    
    def perform_create(self, validated_data):

        with transaction.atomic():

            user = User.objects.create_user(**validated_data)
            Cityzens.objects.create(user=user)

            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])

        return user
    """
    #
    # Create citizen  at polls.signalsAll.s1_Djoser - user_activated
    #
    # Signal is sent after successful user activation.
    #
