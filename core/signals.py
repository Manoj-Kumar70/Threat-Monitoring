from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, Alert


@receiver(post_save, sender=Event)
def create_alert(sender, instance, created, **kwargs):
    if created and instance.severity in ['HIGH', 'CRITICAL']:
        Alert.objects.get_or_create(
            event=instance,
            defaults={'status': 'OPEN'}
        )

