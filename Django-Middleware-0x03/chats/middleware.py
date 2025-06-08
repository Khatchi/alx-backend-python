import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, HttpResponse
from django.utils import timezone
from collections import defaultdict
from threading import Lock

# Configure logger for RequestLoggingMiddleware
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

logger = logging.getLogger(__name__)

# Global storage for tracking messages (in-memory, thread-safe)
message_counts = defaultdict(list)
message_counts_lock = Lock()

class RequestLoggingMiddleware:
    """
    Middleware to log each user's request with timestamp, user, and request path.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to /api/chats/ endpoints outside 6:00 PM to 9:00 PM.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/chats/'):
            current_time = timezone.localtime(timezone.now()).time()
            start_hour = 18  # 6:00 PM
            end_hour = 21    # 9:00 PM
            if not (start_hour <= current_time.hour < end_hour):
                return HttpResponseForbidden(
                    "Access to the messaging app is restricted outside 6:00 PM to 9:00 PM."
                )
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of messages sent per IP address to 5 per minute.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/api/chats/messages/':
            ip_address = request.META.get('REMOTE_ADDR', 'unknown')
            current_time = timezone.now()
            with message_counts_lock:
                message_counts[ip_address] = [
                    timestamp for timestamp in message_counts[ip_address]
                    if current_time - timestamp <= timedelta(minutes=1)
                ]
                if len(message_counts[ip_address]) >= 5:
                    return HttpResponse(
                        "Rate limit exceeded: Maximum 5 messages per minute allowed.",
                        status=429
                    )
                message_counts[ip_address].append(current_time)
        response = self.get_response(request)
        return response

class RolepermissionMiddleware:
    """
    Middleware to restrict DELETE actions on /api/chats/ to admin or moderator roles.
    """
    def __init__(self, get_response):
        """
        Initialize the middleware with the get_response callable.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Check if the user has admin or moderator role for DELETE requests to /api/chats/.
        """
        if request.method == 'DELETE' and request.path.startswith('/api/chats/'):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            # Check if user is admin (is_staff) or in Moderator group
            if not (request.user.is_staff or request.user.groups.filter(name='Moderator').exists()):
                return HttpResponseForbidden(
                    "Only admins or moderators can perform this action."
                )
        response = self.get_response(request)
        return response