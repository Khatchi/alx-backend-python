from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'title': ['icontains'],
        'participants__user_id': ['exact'],
    }

    def get_queryset(self):
        """
        Return conversations where the authenticated user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """
        Ensure the authenticated user is added to the participants when creating a conversation.
        """
        serializer.save()
        participant_ids = serializer.validated_data.get('participant_ids', [])
        if self.request.user.user_id not in participant_ids:
            serializer.instance.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

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
        conversation = serializer.validated_data['conversation']
        if not Conversation.objects.filter(
            conversation_id=conversation.conversation_id,
            participants=self.request.user
        ).exists():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(sender=self.request.user)