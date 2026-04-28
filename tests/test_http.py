"""
Tests for the iSports SDK HTTP client error handling.
"""

import json
import pytest
from unittest.mock import patch, MagicMock

from isports.http import _HTTPClient, _AsyncHTTPClient
from isports.exceptions import (
    ISportsError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    NetworkError,
)


class TestHTTPClientErrorHandling:
    """Test synchronous HTTP client error handling."""

    def setup_method(self):
        self.client = _HTTPClient(api_key="test_key", timeout=30)

    def test_handle_response_success(self):
        """Test successful response with code: 0."""
        data = {"code": 0, "data": ["match1", "match2"]}
        result = self.client._handle_response(data, 200)
        assert result == data

    def test_handle_response_no_code(self):
        """Test response without code field (assumed success)."""
        data = {"data": ["match1"]}
        result = self.client._handle_response(data, 200)
        assert result == data

    def test_handle_response_auth_error_code_2(self):
        """Test auth error with code: 2."""
        data = {"code": 2, "message": "Invalid api_key"}
        with pytest.raises(AuthenticationError) as exc_info:
            self.client._handle_response(data, 200)
        assert "Invalid" in str(exc_info.value)

    def test_handle_response_auth_error_illegal(self):
        """Test auth error with illegal access message."""
        data = {"code": 2, "message": "illegal access"}
        with pytest.raises(AuthenticationError):
            self.client._handle_response(data, 200)

    def test_handle_response_missing_param(self):
        """Test validation error for missing parameters."""
        data = {"code": 1, "message": "Missing parameter 'leagueId'"}
        with pytest.raises(ValidationError) as exc_info:
            self.client._handle_response(data, 200)
        assert "Missing parameter" in str(exc_info.value)

    def test_handle_response_not_found(self):
        """Test 404 response."""
        data = {"message": "not found"}
        with pytest.raises(NotFoundError):
            self.client._handle_response(data, 404)

    def test_handle_response_rate_limit(self):
        """Test 429 rate limit response."""
        data = {"message": "rate limit exceeded"}
        with pytest.raises(RateLimitError):
            self.client._handle_response(data, 429)

    def test_handle_response_server_error(self):
        """Test 500 server error."""
        data = {"message": "Internal Server Error"}
        with pytest.raises(ServerError) as exc_info:
            self.client._handle_response(data, 500)
        assert "500" in str(exc_info.value)

    def test_handle_response_generic_error(self):
        """Test generic error with unknown code."""
        data = {"code": 99, "message": "Something went wrong"}
        with pytest.raises(ISportsError) as exc_info:
            self.client._handle_response(data, 200)
        assert "Something went wrong" in str(exc_info.value)


class TestHTTPClientRequest:
    """Test synchronous HTTP client request methods."""

    def setup_method(self):
        self.client = _HTTPClient(api_key="test_key", timeout=30)

    @patch("urllib.request.urlopen")
    def test_request_success(self, mock_urlopen):
        """Test successful GET request."""
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = json.dumps(
            {"code": 0, "data": []}
        ).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = self.client.request("football", "livescore/today")
        assert result["code"] == 0

    @patch("urllib.request.urlopen")
    def test_request_with_params(self, mock_urlopen):
        """Test request with query parameters."""
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = json.dumps(
            {"code": 0, "data": []}
        ).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        self.client.request(
            "football", "schedule/basic", {"date": "2024-01-15", "leagueId": 39}
        )

        # Verify the request was made with correct URL
        call_args = mock_urlopen.call_args
        req = call_args[0][0]
        assert "api_key=test_key" in req.full_url
        assert "date=2024-01-15" in req.full_url
        assert "leagueId=39" in req.full_url

    @patch("urllib.request.urlopen")
    def test_request_none_params_filtered(self, mock_urlopen):
        """Test that None parameters are filtered out."""
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = json.dumps(
            {"code": 0, "data": []}
        ).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        self.client.request(
            "football", "schedule/basic", {"date": "2024-01-15", "leagueId": None}
        )

        call_args = mock_urlopen.call_args
        req = call_args[0][0]
        assert "date=2024-01-15" in req.full_url
        # None values should be filtered
        assert "leagueId" not in req.full_url or "leagueId=None" not in req.full_url

    @patch("urllib.request.urlopen")
    def test_request_auth_error(self, mock_urlopen):
        """Test handling of authentication error."""
        from urllib.error import HTTPError

        mock_urlopen.side_effect = HTTPError(
            "http://api.isportsapi.com/sport/football/livescore/today?api_key=test_key",
            401,
            "Unauthorized",
            {},
            None,
        )

        with pytest.raises(AuthenticationError):
            self.client.request("football", "livescore/today")

    @patch("urllib.request.urlopen")
    def test_request_network_error(self, mock_urlopen):
        """Test handling of network errors."""
        import urllib.error

        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        with pytest.raises(NetworkError):
            self.client.request("football", "livescore/today")


class TestAsyncHTTPClient:
    """Test async HTTP client."""

    def setup_method(self):
        self.client = _AsyncHTTPClient(api_key="test_key", timeout=30)

    def test_init(self):
        assert self.client.api_key == "test_key"
        assert self.client.timeout == 30
        assert self.client._session is None

    def test_build_url(self):
        url = self.client._build_url("football", "livescore/today")
        assert url == "http://api.isportsapi.com/sport/football/livescore/today"

    @pytest.mark.asyncio
    async def test_close(self):
        """Test closing the async client."""
        await self.client.close()
        assert self.client._session is None

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager."""
        async with _AsyncHTTPClient(api_key="test") as client:
            assert client.api_key == "test"

    @pytest.mark.asyncio
    async def test_import_error_without_aiohttp(self):
        """Test that ImportError is raised when aiohttp is not installed."""
        import builtins
        import sys

        # Remove aiohttp from import cache so the next import hits __import__
        for key in list(sys.modules.keys()):
            if key == "aiohttp" or key.startswith("aiohttp."):
                del sys.modules[key]

        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "aiohttp":
                raise ImportError("No module named 'aiohttp'")
            return original_import(name, *args, **kwargs)

        builtins.__import__ = mock_import
        try:
            client = _AsyncHTTPClient(api_key="test")
            with pytest.raises(ImportError) as exc_info:
                await client.request("football", "livescore/today")
            assert "Async client requires aiohttp" in str(exc_info.value)
        finally:
            builtins.__import__ = original_import
