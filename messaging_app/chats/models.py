from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        """Return a string representation of the user."""
        # return self.username
        return f"User: {self.username}" if self.username else "User: Anonymous"


class Conversation(models.Model):
    """Model representing a conversation between users."""
    title = models.CharField(max_length=100, blank=True, null=True)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the conversation."""
        return self.title if self.title else f"Conversation {self.id}"

    class Meta:
        """Meta options for the Conversation model."""
        ordering = ['-created_at']

class Message(models.Model):
    """Model representing a message in a conversation."""
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the message."""
        return f"Message from {self.sender} in {self.conversation}"

    class Meta:
        """Meta options for the Message model."""
        ordering = ['sent_at']