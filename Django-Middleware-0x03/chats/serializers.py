from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """"Serializer for the User model."""
    class Meta:
        """Meta options for the UserSerializer."""
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']
        read_only_fields = ['user_id', 'created_at', 'updated_at']

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model."""
    sender = UserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    message_body = serializers.CharField() 

    class Meta:
        """Meta options for the MessageSerializer."""
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sender', 'sent_at']

    def create(self, validated_data):
        """
        Custom create method to set the sender to the authenticated user.
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authenticated user is required to send a message.")
        validated_data['sender'] = request.user
        return super().create(validated_data)

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model."""
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )
    title = serializers.CharField(max_length=100, allow_blank=True, required=False)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        """Meta options for the ConversationSerializer."""
        model = Conversation
        fields = ['conversation_id', 'title', 'participants', 'participant_ids', 'messages', 'created_at', 'participant_count']
        read_only_fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def get_participant_count(self, obj):
        """
        Return the number of participants in the conversation.
        """
        return obj.participants.count()

    def validate_participant_ids(self, value):
        """
        Validate that all participant IDs correspond to existing users.
        """
        for user_id in value:
            if not User.objects.filter(user_id=user_id).exists():
                raise serializers.ValidationError(f"User with ID {user_id} does not exist.")
        return value

    def create_participant(self, validated_data):
        """
        Custom create method to handle adding participants to a conversation.
        Expects 'participant_ids' in the request data.
        """
        participant_ids = validated_data.pop('participant_ids')
        title = validated_data.get('title', None)
        conversation = Conversation.objects.create(title=title)

        # Add participants to the conversation
        for user_id in participant_ids:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)

        return conversation

    def update_title_participants(self, validated_data):
        """
        Custom update method to handle updating title and participants.
        """
        conversation = self.instance
        participant_ids = validated_data.pop('participant_ids', None)
        title = validated_data.get('title', conversation.title)

        # Update title if provided
        conversation.title = title
        conversation.save()

        # Update participants if provided
        if participant_ids:
            conversation.participants.clear()
            for user_id in participant_ids:
                user = User.objects.get(user_id=user_id)
                conversation.participants.add(user)

        return conversation