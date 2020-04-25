from .models import Notif, NotifClick
from django.db.models.signals import post_save
from django.dispatch import receiver
import channels.layers
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=NotifClick)
def notif_added(sender, instance, created, update_fields, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notif_user_".format(instance.myuser.id), {
            "type": "notif.send",
            "text": json.dumps({'notif': "New notification"})
        }
    )
