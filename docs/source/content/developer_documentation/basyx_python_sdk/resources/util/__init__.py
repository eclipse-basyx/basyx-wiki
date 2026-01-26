# Utility converters for the API
import base64
from werkzeug.routing import BaseConverter


def base64url_decode(data: str) -> bytes:
    """Decode base64url encoded string."""
    # Add padding if necessary
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data = data + '=' * padding
    # Replace URL-safe characters
    data = data.replace('-', '+').replace('_', '/')
    return base64.b64decode(data)


def base64url_encode(data: bytes) -> str:
    """Encode bytes to base64url string."""
    return base64.urlsafe_b64encode(data).decode('ascii').rstrip('=')


class IdentifierToBase64URLConverter(BaseConverter):
    """Werkzeug URL converter for identifier to base64url."""
    
    def to_python(self, value):
        try:
            return base64url_decode(value)
        except Exception:
            return None
    
    def to_url(self, value):
        return base64url_encode(value)


class IdShortPathConverter(BaseConverter):
    """Werkzeug URL converter for IdShortPath."""
    
    regex = r'[^/]+'
