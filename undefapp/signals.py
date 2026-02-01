# undefapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Transaction, Notification

@receiver(post_save, sender=Transaction)
def create_txn_notification(sender, instance, created, **kwargs):
    """
    • New deposit / withdrawal / transfer               → “submitted” notice  
    • Later status change to approved / rejected        → follow-up notice  
    """
    user = instance.user
    if created:
        msg = f"{instance.get_status_display()} of ${instance.amount} submitted."
    elif instance.status in ("approved", "rejected") and not getattr(instance, "notified", False):
        msg = f"Your {instance.get_status_display()} of ${instance.amount} was {instance.status}."
        instance.notified = True
        instance.save(update_fields=["notified"])
    else:
        return        # nothing new to say

    note = Notification.objects.create(user=user, message=msg)

    # ---- push through WebSocket --------------------
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "message": note.message,
            "timestamp": note.created_at.isoformat(),
        }
    )
