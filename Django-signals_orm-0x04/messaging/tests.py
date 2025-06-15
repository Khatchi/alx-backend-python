from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageNotificationSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='1234')
        self.receiver = User.objects.create_user(username='receiver', password='1234')

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hi there!")
        notification = Notification.objects.filter(user=self.receiver, message=msg)
        self.assertEqual(notification.count(), 1)
        self.assertIn("Hi there", msg.content)