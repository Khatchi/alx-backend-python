from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return conversations where the authenticated user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)
    

    def perform_create(self, serializer):
        serializer.save()
        participant_ids = serializer.validated_data.get('participant_ids', [])
        
        if self.request.user.user_id not in participant_ids:
            serializer.instance.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return messages from conversations where the authenticated user is a participant.
        """
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation')

    def perform_create(self, serializer):
        """
        Create a new message, ensuring it belongs to a valid conversation.
        """
        conversation_id = serializer.validated_data['conversation'].conversation_id
        
        if not Conversation.objects.filter(
            conversation_id=conversation_id,
            participants=self.request.user
        ).exists():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
