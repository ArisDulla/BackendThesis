from django.dispatch import receiver
from djoser.signals import user_activated
from ..models import Cityzens


@receiver(user_activated)
def userActivated(sender, user, request, **kwargs):
    Cityzens.objects.create(user=user)
