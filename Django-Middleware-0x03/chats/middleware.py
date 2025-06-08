import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from django.utils import timezone

# Configure logger for RequestLoggingMiddleware
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

logger = logging.getLogger(__name__)

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
        """
        Initialize the middleware with the get_response callable.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Deny access to /api/chats/ endpoints if outside 6:00 PM to 9:00 PM.
        """
        # Check if the request path starts with /api/chats/
        if request.path.startswith('/api/chats/'):
            current_time = timezone.localtime(timezone.now()).time()
            start_hour = 18  # 6:00 PM
            end_hour = 21    # 9:00 PM

            # Check if current time is outside the allowed window
            if not (start_hour <= current_time.hour < end_hour):
                return HttpResponseForbidden(
                    "Access to the messaging app is restricted outside 6:00 PM to 9:00 PM."
                )

        # Proceed with the request if allowed
        response = self.get_response(request)
        return response