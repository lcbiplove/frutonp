from django.db import models
from frutonp.utils import getUploadTimeDiff

class NotifClick(models.Model):
    myuser = models.OneToOneField('join.MyUser', on_delete=models.CASCADE, related_name='notif_click')
    new_count = models.PositiveIntegerField(default=0, verbose_name='New notifications')

class Notif(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey('posts.Reply', on_delete=models.CASCADE, null=True)
    notif_click = models.ForeignKey(NotifClick, on_delete=models.CASCADE)
    sender = models.ForeignKey('join.MyUser', on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True, verbose_name='Received At')

    def save(self, update_fields=None, *args, **kwargs):
        if update_fields is None:
            self.notif_click.new_count += 1
            self.notif_click.save(update_fields=['new_count'])
        super(Notif, self).save(*args, **kwargs)

    def uploaded_time_for_notif(self):
        output = getUploadTimeDiff(self, longStatus=True)
        return output

    def getUniversalDate(self):
        """ To use external function getUploadTimeDiff in every model, return datetime field of to be calculated
        date time """
        return self.received_at

from django.db.models.signals import post_save
from django.dispatch import receiver
import channels.layers
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=NotifClick)
def notif_added(sender, instance, created, update_fields, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notif_user_{instance.myuser.id}", {
            "type": "notif.send",
            "text": json.dumps({'new_notif': True, 'num': instance.new_count})
        }
    )
