from django_filters import rest_framework as filters
from .models import Message
from django.contrib.auth.models import User
from django.db.models import Q

class MessageFilter(filters.FilterSet):
    """
    Filter messages by conversation participants or time range.
    """
    participant = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        method='filter_by_participant',
        label='Filter by participant user_id'
    )
    start_time = filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='gte',
        label='Messages on or after this time'
    )
    end_time = filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='lte',
        label='Messages on or before this time'
    )

    class Meta:
        model = Message
        fields = ['conversation__conversation_id', 'sender__user_id', 'participant', 'start_time', 'end_time']

    def filter_by_participant(self, queryset, name, value):
        """
        Filter messages where the specified user is a participant in the conversation.
        """
        return queryset.filter(conversation__participants=value)