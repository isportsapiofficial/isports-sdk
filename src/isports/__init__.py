"""
iSports API Python SDK

A comprehensive Python SDK for the iSports API, providing access to
football and basketball sports data.

Reference: https://www.isportsapi.com/en/docs.html
"""

from .client import ISportsClient, ISportsAsyncClient
from .exceptions import (
    ISportsError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ServerError,
    NetworkError,
)

__version__ = "0.1.0"
__author__ = "iSports SDK Team"
__license__ = "MIT"

__all__ = [
    "ISportsClient",
    "ISportsAsyncClient",
    "ISportsError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
    "ServerError",
    "NetworkError",
]
