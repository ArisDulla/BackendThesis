from django.dispatch import receiver
from djoser.signals import user_activated
from ..models import Cityzens
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal
from social_django.models import UserSocialAuth
import random
import string

user_created = Signal()


#
# This signal is sent after successful user activation
#
@receiver(user_activated)
def userActivated(sender, user, request, **kwargs):
    Cityzens.objects.create(user=user)


#
# This signal is sent after successful user registration with social account
#
@receiver(post_save, sender=UserSocialAuth)
def user_created_callback(sender, instance, created, **kwargs):
    if created:

        length = 12
        random_password = "".join(
            random.choices(string.ascii_letters + string.digits, k=length)
        )
        user = instance.user

        # Set the random password for the user
        user.set_password(random_password)
        user.save()

        Cityzens.objects.create(user=instance.user)
