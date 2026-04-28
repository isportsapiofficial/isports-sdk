"""
iSports API Python SDK - Exception Definitions

Defines the exception hierarchy for the SDK.
All exceptions inherit from ISportsError for easy catch-all handling.
"""


class ISportsError(Exception):
    """Base exception for all iSports SDK errors."""

    def __init__(self, message: str = "", response=None):
        super().__init__(message)
        self.message = message
        self.response = response


class AuthenticationError(ISportsError):
    """Raised when API authentication fails (invalid/expired key)."""
    pass


class RateLimitError(ISportsError):
    """Raised when API rate limit is exceeded."""
    pass


class NotFoundError(ISportsError):
    """Raised when requested resource is not found."""
    pass


class ValidationError(ISportsError):
    """Raised when request parameters are invalid or missing."""
    pass


class ServerError(ISportsError):
    """Raised when the API server returns a 5xx error."""
    pass


class NetworkError(ISportsError):
    """Raised when a network-level error occurs (timeout, DNS, etc.)."""
    pass
