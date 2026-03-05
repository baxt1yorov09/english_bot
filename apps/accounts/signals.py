from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from apps.analytics.models import UserActivityLog

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        # Log user registration
        UserActivityLog.objects.create(
            user=instance,
            action='register',
            metadata={
                'telegram_id': instance.telegram_id,
                'username': instance.telegram_username,
                'level': instance.current_level
            }
        )
