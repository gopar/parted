from django.contrib.messages.storage.fallback import FallbackStorage


def add_message_middleware(request):
    """Add message middleware to request"""
    setattr(request, "session", "session")
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    return request
