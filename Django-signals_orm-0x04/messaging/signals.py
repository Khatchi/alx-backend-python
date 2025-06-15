from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f"You have a new message from {instance.sender.username}."
        )


@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    # Only check for updates to existing messages
    if instance.id:
        try:
            old_instance = Message.objects.get(id=instance.id)
            if old_instance.content != instance.content:
                # Log the old content to history
                MessageHistory.objects.create(
                    message=old_instance,
                    old_content=old_instance.content,
                    edited_by=instance.edited_by
                )
                # Mark message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications related to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message history the user edited
    MessageHistory.objects.filter(edited_by=instance).delete()