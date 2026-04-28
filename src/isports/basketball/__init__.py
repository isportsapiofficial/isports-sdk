"""
iSports API Python SDK - Basketball Module

Provides access to all Basketball API endpoints.
Organized by functional category.
"""

from typing import Optional, Dict, Any


class BasketballLiveData:
    """Basketball Live Data APIs - real-time match information."""

    def __init__(self, http_client):
        self._http = http_client

    def livescores(self) -> Dict[str, Any]:
        """
        Get today's basketball livescores (GMT+0 00:00-23:59).

        Use with livescore_changes() for efficient polling.
        """
        return self._http.request("basketball", "livescores")

    def livescore_changes(self) -> Dict[str, Any]:
        """
        Get livescore changes updated in the last 15 seconds.

        Use with livescores() for efficient polling.
        """
        return self._http.request("basketball", "livescores/changes")

    def schedule(
        self,
        date: Optional[str] = None,
        league_id: Optional[int] = None,
        match_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get basketball schedule and results.

        Args:
            date: Date in yyyy-MM-dd format (from last 2 months to future)
            league_id: League ID
            match_id: Specific match ID

        Note: Only one of date/league_id/match_id should be provided.
        """
        params = {}
        if date:
            params["date"] = date
        if league_id:
            params["leagueId"] = league_id
        if match_id:
            params["matchId"] = match_id
        return self._http.request("basketball", "schedule", params)

    def schedule_basic(
        self,
        date: Optional[str] = None,
        league_id: Optional[int] = None,
        match_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get basic schedule and results information.

        Args:
            date: Date in yyyy-MM-dd format
            league_id: League ID
            match_id: Specific match ID
        """
        params = {}
        if date:
            params["date"] = date
        if league_id:
            params["leagueId"] = league_id
        if match_id:
            params["matchId"] = match_id
        return self._http.request("basketball", "schedule/basic", params)

    def lineups(self, match_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get basketball match lineups and injuries (last 24h + future 48h).

        Args:
            match_id: Specific match ID
        """
        params = {}
        if match_id:
            params["matchId"] = match_id
        return self._http.request("basketball", "lineups", params)

    def today_match(self) -> Dict[str, Any]:
        """
        Get today's basketball match list.
        """
        return self._http.request("basketball", "today/match")

    def livetext_list(self) -> Dict[str, Any]:
        """
        Get live text match list of today and past 8 hours (NBA/WNBA only).

        Use with livetext() for content.
        """
        return self._http.request("basketball", "livetext/list")

    def livetext(self, match_id: int) -> Dict[str, Any]:
        """
        Get live text content for a specific match (NBA/WNBA only).

        Args:
            match_id: Match ID
        """
        return self._http.request("basketball", "livetext", {"matchId": match_id})


class BasketballProfile:
    """Basketball Profile APIs - league, team, player information."""

    def __init__(self, http_client):
        self._http = http_client

    def team(self, team_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get team information.

        Args:
            team_id: Specific team ID. If not provided, returns all teams.
        """
        params = {}
        if team_id:
            params["teamId"] = team_id
        return self._http.request("basketball", "team", params)

    def team_search(self, name: str) -> Dict[str, Any]:
        """
        Search teams by name.

        Args:
            name: Team name (partial match supported)
        """
        return self._http.request("basketball", "team/search", {"name": name})

    def player(self, player_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get player information.

        Args:
            player_id: Specific player ID. If not provided, returns all players.
        """
        params = {}
        if player_id:
            params["playerId"] = player_id
        return self._http.request("basketball", "player", params)

    def player_search(self, name: str) -> Dict[str, Any]:
        """
        Search players by name.

        Args:
            name: Player name (partial match supported)
        """
        return self._http.request("basketball", "player/search", {"name": name})

    def league(self) -> Dict[str, Any]:
        """
        Get complete information of all basketball leagues and cups.
        """
        return self._http.request("basketball", "league")

    def league_basic(self) -> Dict[str, Any]:
        """
        Get basic information of all basketball leagues and cups.
        """
        return self._http.request("basketball", "league/basic")

    def cupqualify(self) -> Dict[str, Any]:
        """
        Get stage type information for different cups.
        """
        return self._http.request("basketball", "cupqualify")

    def playoffs(self) -> Dict[str, Any]:
        """
        Get playoff-type information of different leagues.
        """
        return self._http.request("basketball", "playoffs")

    def transfer(self, day: Optional[int] = None) -> Dict[str, Any]:
        """
        Get NBA transfer records.

        Args:
            day: Return transfer data within n days (e.g. day=7)
        """
        params = {}
        if day is not None:
            params["day"] = day
        return self._http.request("basketball", "transfer", params)


class BasketballStats:
    """Basketball Statistics APIs - standings, match stats, analysis."""

    def __init__(self, http_client):
        self._http = http_client

    def standing(self, league_id: str) -> Dict[str, Any]:
        """
        Get league standings.

        Args:
            league_id: League ID (string, required)
        """
        return self._http.request("basketball", "standing/league", {"leagueId": league_id})

    def cup_standing(self, league_id: str) -> Dict[str, Any]:
        """
        Get cup ranking data.

        Args:
            league_id: League/Cup ID (string, required). Parameter name is leagueId.
        """
        return self._http.request("basketball", "standing/cup", {"leagueId": league_id})

    def stats(
        self,
        match_id: Optional[int] = None,
        date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get match technical statistics (default: matches within 24h).

        Args:
            match_id: Specific match ID
            date: Date in yyyy-MM-dd format

        Note: Player stats currently supports NBA, WNBA, CBA, and other major leagues.
        """
        params = {}
        if match_id:
            params["matchId"] = match_id
        if date:
            params["date"] = date
        return self._http.request("basketball", "stats", params)

    def quarters_stats(
        self,
        match_id: Optional[int] = None,
        date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get single-quarter statistics for basketball matches (NBA and similar).

        Args:
            match_id: Specific match ID
            date: Date in yyyy-MM-dd format (limited to past week)
        """
        params = {"cmd": "stats"}
        if match_id:
            params["matchId"] = match_id
        if date:
            params["date"] = date
        return self._http.request("basketball", "stats", params)

    def analysis(self, match_id: int) -> Dict[str, Any]:
        """
        Get match analysis data (past 7 days + next 7 days).

        Includes H2H, last match, and future schedule.
        Data cached for 24 hours.

        Args:
            match_id: Match ID (required)
        """
        return self._http.request("basketball", "analysis", {"matchId": match_id})


class BasketballOdds:
    """Basketball Odds APIs."""

    def __init__(self, http_client):
        self._http = http_client

    def fulltime(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get full-time odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("basketball", "odds/fulltime", params)

    def fulltime_changes(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get full-time odds changes."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("basketball", "odds/fulltime/changes", params)

    def half(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get half-time odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("basketball", "odds/half", params)

    def quarter(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get quarter odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("basketball", "odds/quarter", params)

    def history(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get historical odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("basketball", "odds/history", params)

    def european_all(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get European odds from 200+ bookmakers."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("basketball", "odds/european/all", params)

    def inplay(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get in-play odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("basketball", "odds/inplay", params)


class BasketballCommon:
    """Basketball Common APIs - utility endpoints."""

    def __init__(self, http_client):
        self._http = http_client

    def country(self) -> Dict[str, Any]:
        """Get list of all countries and country IDs."""
        return self._http.request("basketball", "country")

    def bookmaker(self) -> Dict[str, Any]:
        """Get list of all bookmakers and bookmaker IDs."""
        return self._http.request("basketball", "bookmaker")

    def schedule_modify(self) -> Dict[str, Any]:
        """Get schedule deletion and match time modification records (past 24h)."""
        return self._http.request("basketball", "schedule/modify")


class BasketballAPI:
    """Basketball API aggregate - provides access to all basketball endpoints."""

    def __init__(self, http_client):
        self._http = http_client
        self.live_data = BasketballLiveData(http_client)
        self.profile = BasketballProfile(http_client)
        self.stats = BasketballStats(http_client)
        self.odds = BasketballOdds(http_client)
        self.common = BasketballCommon(http_client)
