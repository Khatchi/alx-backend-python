import logging
from datetime import datetime

# Configure logger
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
        """
        Initialize the middleware with the get_response callable.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Log the request details: timestamp, user, and path.
        """
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        
        # Process the request and get the response
        response = self.get_response(request)
        return response