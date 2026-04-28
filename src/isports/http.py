"""
iSports API Python SDK - HTTP Client

Handles all HTTP communication with the iSports API.
Provides both synchronous and asynchronous interfaces.
"""

from typing import Optional, Dict, Any
import json

from .exceptions import (
    ISportsError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ServerError,
    NetworkError,
)


class _HTTPClient:
    """Internal synchronous HTTP client."""

    BASE_URL = "http://api.isportsapi.com/sport"

    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout

    def _build_url(self, sport: str, endpoint: str) -> str:
        """Build the full API URL for a given sport and endpoint."""
        return f"{self.BASE_URL}/{sport}/{endpoint}"

    def _handle_response(self, response_data: Dict[str, Any], status_code: int) -> Dict[str, Any]:
        """Parse and validate API response, raising appropriate exceptions on errors."""
        # iSports API returns 200 with error message in body for auth failures
        if status_code == 200 and isinstance(response_data, dict):
            code = response_data.get("code")
            message = response_data.get("message", "")
            
            # code 0 = success, code 2 = invalid api_key
            if code == 0 or "code" not in response_data:
                return response_data
            
            if code == 2 or "Invalid" in message or "illegal access" in message:
                raise AuthenticationError(message, response_data)
            if "Missing parameter" in message or "parameter" in message.lower():
                raise ValidationError(message, response_data)
            if "not found" in message.lower():
                raise NotFoundError(message, response_data)
            if "rate limit" in message.lower() or "too many" in message.lower():
                raise RateLimitError(message, response_data)
            
            # Generic error with code
            raise ISportsError(message, response_data)

        if status_code == 401:
            raise AuthenticationError("Unauthorized: Invalid API key", response_data)
        if status_code == 403:
            raise AuthenticationError("Forbidden: Access denied", response_data)
        if status_code == 404:
            raise NotFoundError("Resource not found", response_data)
        if status_code == 429:
            raise RateLimitError("Rate limit exceeded", response_data)
        if status_code == 422:
            raise ValidationError("Invalid request parameters", response_data)
        if status_code >= 500:
            raise ServerError(f"Server error: {status_code}", response_data)

        return response_data

    def request(
        self,
        sport: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
    ) -> Dict[str, Any]:
        """Make a synchronous HTTP request to the API."""
        import urllib.request
        import urllib.parse
        import urllib.error
        import socket

        url = self._build_url(sport, endpoint)
        
        # Build query parameters
        query_params = {"api_key": self.api_key}
        if params:
            # Filter out None values
            query_params.update({k: v for k, v in params.items() if v is not None})
        
        query_string = urllib.parse.urlencode(query_params, doseq=True)
        full_url = f"{url}?{query_string}"

        req = urllib.request.Request(
            full_url,
            method=method.upper(),
            headers={
                "Accept": "application/json",
                "User-Agent": "isports-sdk-python/0.1.0",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                status_code = resp.getcode()
                body = resp.read().decode("utf-8")
                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    data = {"raw": body}
                return self._handle_response(data, status_code)
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode("utf-8")
                data = json.loads(body)
            except Exception:
                data = {"raw": body if 'body' in dir() else str(e)}
            return self._handle_response(data, e.code)
        except urllib.error.URLError as e:
            raise NetworkError(f"Network error: {e.reason}") from e
        except socket.timeout:
            raise NetworkError("Request timed out") from None
        except Exception as e:
            raise NetworkError(f"Unexpected error: {str(e)}") from e


class _AsyncHTTPClient:
    """Internal asynchronous HTTP client (requires aiohttp)."""

    BASE_URL = "http://api.isportsapi.com/sport"

    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self._session = None

    def _build_url(self, sport: str, endpoint: str) -> str:
        return f"{self.BASE_URL}/{sport}/{endpoint}"

    def _handle_response(self, response_data: Dict[str, Any], status_code: int) -> Dict[str, Any]:
        """Parse and validate API response."""
        if status_code == 200 and isinstance(response_data, dict):
            code = response_data.get("code")
            message = response_data.get("message", "")
            
            if code == 0 or "code" not in response_data:
                return response_data
            
            if code == 2 or "Invalid" in message or "illegal access" in message:
                raise AuthenticationError(message, response_data)
            if "Missing parameter" in message or "parameter" in message.lower():
                raise ValidationError(message, response_data)
            if "not found" in message.lower():
                raise NotFoundError(message, response_data)
            if "rate limit" in message.lower():
                raise RateLimitError(message, response_data)
            
            raise ISportsError(message, response_data)

        if status_code == 401:
            raise AuthenticationError("Unauthorized: Invalid API key", response_data)
        if status_code == 403:
            raise AuthenticationError("Forbidden: Access denied", response_data)
        if status_code == 404:
            raise NotFoundError("Resource not found", response_data)
        if status_code == 429:
            raise RateLimitError("Rate limit exceeded", response_data)
        if status_code == 422:
            raise ValidationError("Invalid request parameters", response_data)
        if status_code >= 500:
            raise ServerError(f"Server error: {status_code}", response_data)

        return response_data

    async def request(
        self,
        sport: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
    ) -> Dict[str, Any]:
        """Make an asynchronous HTTP request to the API."""
        try:
            import aiohttp
        except ImportError:
            raise ImportError(
                "Async client requires aiohttp. Install with: pip install aiohttp"
            )

        url = self._build_url(sport, endpoint)
        
        query_params = {"api_key": self.api_key}
        if params:
            query_params.update({k: v for k, v in params.items() if v is not None})

        if self._session is None:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)

        try:
            async with self._session.request(
                method=method.upper(),
                url=url,
                params=query_params,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "isports-sdk-python/0.1.0",
                },
            ) as resp:
                status_code = resp.status
                try:
                    data = await resp.json()
                except Exception:
                    text = await resp.text()
                    data = {"raw": text}
                return self._handle_response(data, status_code)
        except aiohttp.ClientResponseError as e:
            raise NetworkError(f"HTTP error: {e.status} {e.message}") from e
        except aiohttp.ClientError as e:
            raise NetworkError(f"Network error: {str(e)}") from e
        except TimeoutError:
            raise NetworkError("Request timed out") from None

    async def close(self):
        """Close the async session."""
        if self._session:
            await self._session.close()
            self._session = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
