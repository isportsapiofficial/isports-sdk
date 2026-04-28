"""
iSports API Python SDK - Main Client

Provides high-level access to the iSports API.
Usage:
    >>> from isports import ISportsClient
    >>> client = ISportsClient(api_key="your_key")
    >>> scores = client.football.live_data.livescore_today()
"""

from typing import Optional

from .http import _HTTPClient, _AsyncHTTPClient
from .football import FootballAPI
from .basketball import BasketballAPI


class ISportsClient:
    """
    Synchronous client for the iSports API.

    Provides access to Football and Basketball APIs through organized sub-clients:
    - client.football.live_data - Live scores, schedules, events
    - client.football.profile   - League, team, player info
    - client.football.stats     - Standings, player stats, analysis
    - client.football.odds      - Pre-match, in-play, historical odds
    - client.football.common    - Utility endpoints
    - client.basketball.live_data - Basketball live data
    - client.basketball.profile   - Basketball profiles
    - client.basketball.stats     - Basketball statistics

    Args:
        api_key: Your iSports API key
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> client = ISportsClient(api_key="your_api_key")
        >>> # Get today's football livescores
        >>> scores = client.football.live_data.livescore_today()
        >>> # Get basketball schedule
        >>> schedule = client.basketball.live_data.schedule(date="2024-01-15")
    """

    def __init__(self, api_key: str, timeout: int = 30):
        if not api_key or not isinstance(api_key, str):
            raise ValueError("api_key must be a non-empty string")
        
        self.api_key = api_key
        self.timeout = timeout
        self._http = _HTTPClient(api_key=api_key, timeout=timeout)
        self.football = FootballAPI(self._http)
        self.basketball = BasketballAPI(self._http)

    def __repr__(self) -> str:
        return f"<ISportsClient api_key=*** timeout={self.timeout}>"


class ISportsAsyncClient:
    """
    Asynchronous client for the iSports API.

    Provides the same functionality as ISportsClient but with async support.
    Requires aiohttp to be installed.

    Args:
        api_key: Your iSports API key
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> async with ISportsAsyncClient(api_key="your_api_key") as client:
        ...     scores = await client.football.live_data.livescore_today()
    """

    def __init__(self, api_key: str, timeout: int = 30):
        if not api_key or not isinstance(api_key, str):
            raise ValueError("api_key must be a non-empty string")
        
        self.api_key = api_key
        self.timeout = timeout
        self._http = _AsyncHTTPClient(api_key=api_key, timeout=timeout)
        self.football = FootballAPI(self._http)
        self.basketball = BasketballAPI(self._http)

    def __repr__(self) -> str:
        return f"<ISportsAsyncClient api_key=*** timeout={self.timeout}>"

    async def close(self):
        """Close the underlying async HTTP session."""
        await self._http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
