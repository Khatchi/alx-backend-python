from rest_framework import permissions

from .models import Conversation

class IsConversationParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # For Conversation objects
        if isinstance(obj, Conversation):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        # For Message objects
        return obj.conversation.participants.filter(user_id=request.user.user_id).exists()