import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """Custom user model that extends Django's AbstractUser."""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the user."""
        return f"User: {self.username} (ID: {self.user_id})"\
        if self.username else "User: Anonymous"

    class Meta:
        """Meta options for the User model."""
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username'], name='idx_user_username'),
            models.Index(fields=['email'], name='idx_user_email'),
        ]

class Conversation(models.Model):
    """Model representing a conversation between users."""
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    title = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the conversation."""
        return self.title if self.title else f"Conversation {self.conversation_id}"

    class Meta:
        """Meta options for the Conversation model."""
        ordering = ['-created_at']

class Message(models.Model):
    """Model representing a message in a conversation.""" 
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the message."""
        return f"Message from {self.sender} in {self.conversation}"

    class Meta:
        """Meta options for the Message model."""
        ordering = ['sent_at']