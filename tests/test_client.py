"""
Tests for the iSports SDK client.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from isports import ISportsClient, ISportsAsyncClient
from isports.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    NetworkError,
)


class TestISportsClient:
    """Test synchronous client."""

    def test_init(self):
        client = ISportsClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.timeout == 30

    def test_init_invalid_key(self):
        with pytest.raises(ValueError):
            ISportsClient(api_key="")
        with pytest.raises(ValueError):
            ISportsClient(api_key=None)

    def test_football_live_data(self):
        client = ISportsClient(api_key="test_key")
        assert client.football.live_data is not None
        assert client.football.profile is not None
        assert client.football.stats is not None
        assert client.football.odds is not None
        assert client.football.common is not None

    def test_basketball_api(self):
        client = ISportsClient(api_key="test_key")
        assert client.basketball.live_data is not None
        assert client.basketball.profile is not None
        assert client.basketball.stats is not None
        assert client.basketball.odds is not None
        assert client.basketball.common is not None

    @patch("isports.http._HTTPClient.request")
    def test_livescores(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        client = ISportsClient(api_key="test_key")
        result = client.football.live_data.livescores()
        mock_request.assert_called_once_with("football", "livescores")
        assert result["code"] == 0

    @patch("isports.http._HTTPClient.request")
    def test_schedule_with_params(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        client = ISportsClient(api_key="test_key")
        client.football.live_data.schedule_basic(date="2024-01-15", league_id="123")
        mock_request.assert_called_once_with(
            "football", "schedule/basic", {"date": "2024-01-15", "leagueId": "123"}
        )


class TestAuthenticationErrors:
    """Test authentication error handling."""

    @patch("isports.http._HTTPClient.request")
    def test_auth_error(self, mock_request):
        mock_request.side_effect = AuthenticationError("Invalid api_key")
        client = ISportsClient(api_key="bad_key")
        with pytest.raises(AuthenticationError):
            client.football.live_data.livescores()


class TestAsyncClient:
    """Test async client (requires aiohttp)."""

    @pytest.mark.asyncio
    async def test_async_init(self):
        client = ISportsAsyncClient(api_key="test_key")
        assert client.api_key == "test_key"
        await client.close()

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        async with ISportsAsyncClient(api_key="test_key") as client:
            assert client.api_key == "test_key"


class TestFootballOdds:
    """Test football odds endpoints."""

    @patch("isports.http._HTTPClient.request")
    def test_main(self, mock_request):
        mock_request.return_value = {"code": 0, "data": {}}
        client = ISportsClient(api_key="test_key")
        client.football.odds.main(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "odds/main", {"matchId": 12345}
        )

    @patch("isports.http._HTTPClient.request")
    def test_european_all(self, mock_request):
        mock_request.return_value = {"code": 0, "data": {}}
        client = ISportsClient(api_key="test_key")
        client.football.odds.european_all(league_id=39)
        mock_request.assert_called_once_with(
            "football", "odds/european/all", {"leagueId": 39}
        )


class TestBasketball:
    """Test basketball endpoints."""

    @patch("isports.http._HTTPClient.request")
    def test_basketball_livescores(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        client = ISportsClient(api_key="test_key")
        result = client.basketball.live_data.livescores()
        mock_request.assert_called_once_with("basketball", "livescores")
        assert result["code"] == 0

    @patch("isports.http._HTTPClient.request")
    def test_basketball_schedule(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        client = ISportsClient(api_key="test_key")
        client.basketball.live_data.schedule(date="2024-01-15")
        mock_request.assert_called_once_with(
            "basketball", "schedule", {"date": "2024-01-15"}
        )


class TestCommonEndpoints:
    """Test common utility endpoints."""

    @patch("isports.http._HTTPClient.request")
    def test_country(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        client = ISportsClient(api_key="test_key")
        client.football.common.country()
        mock_request.assert_called_once_with("football", "country")

    @patch("isports.http._HTTPClient.request")
    def test_schedule_modify(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        client = ISportsClient(api_key="test_key")
        client.football.common.schedule_modify()
        mock_request.assert_called_once_with("football", "schedule/modify")
