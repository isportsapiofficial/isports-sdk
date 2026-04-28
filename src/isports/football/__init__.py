"""
iSports API Python SDK - Football Module

Provides access to all Football API endpoints.
Organized by functional category.
"""

from typing import Optional, Dict, Any


class FootballLiveData:
    """Football Live Data APIs - real-time match information."""

    def __init__(self, http_client):
        self._http = http_client

    def livescores(self) -> Dict[str, Any]:
        """
        Get today's football livescores (GMT+0 00:00-23:59).

        Returns match status, scores, corners, cards, etc.
        """
        return self._http.request("football", "livescores")

    def livescore_changes(self) -> Dict[str, Any]:
        """
        Get livescore changes updated in the last 20 seconds.

        Use with livescores() for efficient polling.
        """
        return self._http.request("football", "livescores/changes")

    def schedule_basic(
        self,
        date: Optional[str] = None,
        league_id: Optional[str] = None,
        season: Optional[str] = None,
        match_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get schedule and results with basic information.

        Args:
            date: Date in yyyy-MM-dd format
            league_id: League/cup ID (string)
            season: Use with league_id to get specified season, e.g. "2018-2019"
            match_id: Specific match ID (string)

        Note: Only one of date/league_id/match_id should be provided.
        """
        params = {}
        if date:
            params["date"] = date
        if league_id:
            params["leagueId"] = league_id
        if season:
            params["season"] = season
        if match_id:
            params["matchId"] = match_id
        return self._http.request("football", "schedule/basic", params)

    def schedule(
        self,
        date: Optional[str] = None,
        league_id: Optional[str] = None,
        season: Optional[str] = None,
        sub_league_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        match_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get detailed schedule and results.

        Args:
            date: Date in yyyy-MM-dd format
            league_id: League/cup ID (string)
            season: Use with league_id to get specified season, e.g. "2018-2019"
            sub_league_id: Use with league_id to get specified sub league
            stage_id: Use with league_id to get specified cup stage
            match_id: Specific match ID(s), multiple IDs separated by ","
        """
        params = {}
        if date:
            params["date"] = date
        if league_id:
            params["leagueId"] = league_id
        if season:
            params["season"] = season
        if sub_league_id:
            params["subLeagueId"] = sub_league_id
        if stage_id:
            params["stageId"] = stage_id
        if match_id:
            params["matchId"] = match_id
        return self._http.request("football", "schedule", params)

    def events(
        self,
        date: Optional[str] = None,
        cmd: bool = False,
    ) -> Dict[str, Any]:
        """
        Get instant match events (goals, cards, substitutions, etc.).

        Args:
            date: Date in yyyy-MM-dd format (only for matches in the past one month)
            cmd: If True, returns only data updated in the last 3 minutes
        """
        params = {}
        if date:
            params["date"] = date
        if cmd:
            params["cmd"] = "new"
        return self._http.request("football", "events", params)

    def events_corner(self) -> Dict[str, Any]:
        """
        Get corner kick events for matches.
        """
        return self._http.request("football", "events/corner")

    def lineups(
        self,
        match_id: Optional[str] = None,
        is_preview: bool = False,
    ) -> Dict[str, Any]:
        """
        Get match lineups (starting XI, substitutes, injuries).

        Args:
            match_id: Specific match ID (string)
            is_preview: If True, returns preview lineup (fixed value: true)
        """
        params = {}
        if match_id:
            params["matchId"] = match_id
        if is_preview:
            params["isPreview"] = "true"
        return self._http.request("football", "lineups", params)

    def injury(self) -> Dict[str, Any]:
        """
        Get injury and suspension list (past 8 hours + next 3 days).
        """
        return self._http.request("football", "injury")

    def livetext_list(self) -> Dict[str, Any]:
        """
        Get live text match list for today and past 8 hours.

        Use with livetext() for content.
        """
        return self._http.request("football", "livetext/list")

    def livetext(self, match_id: int) -> Dict[str, Any]:
        """
        Get live text commentary for a specific match.

        Args:
            match_id: Specific match ID
        """
        return self._http.request("football", "livetext", {"matchId": match_id})


class FootballProfile:
    """Football Profile APIs - league, team, player information."""

    def __init__(self, http_client):
        self._http = http_client

    def league_basic(self) -> Dict[str, Any]:
        """
        Get basic information of all leagues and cups.

        Returns 2000+ football leagues & cups with IDs and metadata.
        """
        return self._http.request("football", "league/basic")

    def league(self) -> Dict[str, Any]:
        """
        Get complete information of all leagues and cups.
        """
        return self._http.request("football", "league")

    def league_sub(self) -> Dict[str, Any]:
        """
        Get sub-league information.
        """
        return self._http.request("football", "league/sub")

    def league_stage(self) -> Dict[str, Any]:
        """
        Get cup stage information.
        """
        return self._http.request("football", "league/stage")

    def team(self, team_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get team information.

        Args:
            team_id: Specific team ID. If not provided, returns all teams.
        """
        params = {}
        if team_id:
            params["teamId"] = team_id
        return self._http.request("football", "team", params)

    def team_search(self, name: str) -> Dict[str, Any]:
        """
        Search teams by name.

        Args:
            name: Team name (partial match supported)
        """
        return self._http.request("football", "team/search", {"name": name})

    def player(
        self,
        team_id: Optional[int] = None,
        day: Optional[str] = None,
        player_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get player information.

        Args:
            team_id: Filter by team ID
            day: Date in yyyy-MM-dd format
            player_id: Specific player ID

        Note: Only one parameter should be provided.
        """
        params = {}
        if team_id:
            params["teamId"] = team_id
        if day:
            params["day"] = day
        if player_id:
            params["playerId"] = player_id
        return self._http.request("football", "player", params)

    def player_search(self, name: str) -> Dict[str, Any]:
        """
        Search players by name.

        Args:
            name: Player name (partial match supported)
        """
        return self._http.request("football", "player/search", {"name": name})

    def referee(self) -> Dict[str, Any]:
        """
        Get referee data for matches in the past 24 hours to future.
        """
        return self._http.request("football", "referee")

    def transfer(self, league_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get transfer information for Big Five Leagues.

        Args:
            league_id: Specific league ID
        """
        params = {}
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "transfer", params)


class FootballStats:
    """Football Statistics APIs - standings, player stats, analysis."""

    def __init__(self, http_client):
        self._http = http_client

    def standing(self, league_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get league standings.

        Args:
            league_id: League ID. Without parameter, returns leagues updated in last 24h.
        """
        params = {}
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "standing/league", params)

    def cup_standing(self, cup_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get cup group stage standings.

        Args:
            cup_id: Cup ID. Without parameter, returns cups updated in last 24h.
        """
        params = {}
        if cup_id:
            params["cupId"] = cup_id
        return self._http.request("football", "standing/cup", params)

    def subleague_standing(self, league_id: int) -> Dict[str, Any]:
        """
        Get subleague standings when a league has multiple divisions/stages.

        Args:
            league_id: League ID
        """
        return self._http.request("football", "standing/league/getsub", {"leagueId": league_id})

    def topscorer(self, league_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get top scorers for a league/cup.

        Args:
            league_id: League/cup ID
        """
        params = {}
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "topscorer", params)

    def analysis(self, match_id: int) -> Dict[str, Any]:
        """
        Get match analysis data for a specific match.

        Includes H2H, last matches, future schedule, odds stats, goals stats.
        Data cached for 24 hours.

        Args:
            match_id: Match ID (required)
        """
        return self._http.request("football", "analysis", {"matchId": match_id})

    def playerstats_match_list(self) -> Dict[str, Any]:
        """
        Get list of matches with player technical statistics within 24h.

        Use with playerstats_match() for detailed stats.
        """
        return self._http.request("football", "playerstats/match/list")

    def playerstats_match(self, match_id: int) -> Dict[str, Any]:
        """
        Get player technical statistics for a specific match.

        Args:
            match_id: Match ID
        """
        return self._http.request("football", "playerstats/match", {"matchId": match_id})

    def playerstats_league_list(self) -> Dict[str, Any]:
        """
        Get list of leagues with player seasonal technical statistics.

        Use with playerstats_league() for detailed stats.
        """
        return self._http.request("football", "playerstats/league/list")

    def playerstats_league(self, league_id: int) -> Dict[str, Any]:
        """
        Get player seasonal technical statistics for a league.

        Args:
            league_id: League/cup ID

        Note: Data distinguishes home/away, total needs aggregation.
        """
        return self._http.request("football", "playerstats/league", {"leagueId": league_id})


class FootballOdds:
    """Football Odds APIs - pre-match, in-play, and historical odds."""

    def __init__(self, http_client):
        self._http = http_client

    # Main Odds (18 bookmakers)
    def main(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get main market odds from 18 bookmakers (Asian, 1x2, OU)."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/main", params)

    def main_changes(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get main market odds changes."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/main/changes", params)

    def main_future(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get future main market odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/main/future", params)

    def main_history(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get historical main market odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/main/history", params)

    # All Odds
    def all_odds(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get all odds (Asian, 1x2, OU from more bookmakers)."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/all", params)

    def all_changes(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get all odds changes."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/all/changes", params)

    def all_future(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get future all odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/all/future", params)

    def all_history(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get historical all odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/all/history", params)

    # In-play Odds
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
        return self._http.request("football", "odds/inplay", params)

    def inplay_half(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get in-play halftime odds (handicapHalf, europeOddHalf, overUnderHalf)."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/inplay/half", params)

    # European Odds (200+ Bookmakers)
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
        return self._http.request("football", "odds/european/all", params)

    def european_half(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get halftime European odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/european/half", params)

    # Odds by Match ID
    def odds_by_id(
        self,
        match_id: int,
        company_id: Optional[int] = None,
        odds_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get historical odds by match ID and company ID.

        Args:
            match_id: Match ID
            company_id: Bookmaker company ID
            odds_type: "multi" for multi-market, omit for main market
        """
        params = {"matchId": match_id}
        if company_id is not None:
            params["companyID"] = company_id
        if odds_type:
            params["type"] = odds_type
        return self._http.request("football", "odds/oddsbyid", params)

    # Outrights & Specials
    def outrights(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get outrights and special odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/outrights", params)

    def halffull_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match half time / full time odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/halffull/prematch", params)

    def halffull_inplay(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get in-play half time / full time odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/halffull/inplay", params)

    def teamtoscore_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match team to score odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/teamtoscore/prematch", params)

    def teamtoscore_inplay(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get in-play team to score odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/teamtoscore/inplay", params)

    def oddeven_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match odd/even goals odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/oddeven/prematch", params)

    def oddeven_inplay(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get in-play odd/even goals odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/oddeven/inplay", params)

    def totalgoals_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match total goals odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/totalgoals/prematch", params)

    def totalgoals_inplay(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get in-play total goals odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/totalgoals/inplay", params)

    def score_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match correct score odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/score/prematch", params)

    def score_half_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match half-time correct score odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/score/half/prematch", params)

    def score_inplay(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get in-play correct score odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/score/inplay", params)

    def score_half_inplay(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get in-play half-time correct score odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/score/half/inplay", params)

    def cornershandicap_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match corners handicap odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/cornershandicap/prematch", params)

    def cornershandicap_inplay(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get in-play corners handicap odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/cornershandicap/inplay", params)

    def cornerstotal_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match total corners odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/cornerstotal/prematch", params)

    def cornerstotal_inplay(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get in-play total corners odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/cornerstotal/inplay", params)

    def corners_1x2_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match corners 1x2 odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/corners1x2/prematch", params)

    def kickoff_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match kickoff odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/kickoff/prematch", params)

    def team_goals(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get team goals odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/teamGoals", params)

    def both_score(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get both teams to score odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/bothScore", params)

    def card(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get card odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/card", params)

    def books(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get book odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/books", params)

    def eurohandicap_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match Euro handicap odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/eurohandicap/prematch", params)

    def doublechance_prematch(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get pre-match double chance odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "odds/doublechance/prematch", params)

    def betfair(
        self,
        match_id: Optional[int] = None,
        league_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get Betfair exchange odds."""
        params = {}
        if match_id:
            params["matchId"] = match_id
        if league_id:
            params["leagueId"] = league_id
        return self._http.request("football", "betfair", params)


class FootballCommon:
    """Football Common APIs - utility endpoints available with any paid plan."""

    def __init__(self, http_client):
        self._http = http_client

    def team_modify(self) -> Dict[str, Any]:
        """Get team ID merge and deletion records (last 7 days)."""
        return self._http.request("football", "team/modify")

    def player_modify(self) -> Dict[str, Any]:
        """Get player ID merge and deletion records (last 7 days)."""
        return self._http.request("football", "player/modify")

    def schedule_modify(self) -> Dict[str, Any]:
        """Get schedule deletion and match time modification records (last 12 hours)."""
        return self._http.request("football", "schedule/modify")

    def country(self) -> Dict[str, Any]:
        """Get list of all countries and country IDs."""
        return self._http.request("football", "country")

    def bookmaker(self) -> Dict[str, Any]:
        """Get list of all bookmakers and bookmaker IDs."""
        return self._http.request("football", "bookmaker")

    def fifaranking(self) -> Dict[str, Any]:
        """Get FIFA ranking data."""
        return self._http.request("football", "fifaranking")

    def summary(self) -> Dict[str, Any]:
        """Get match summary data."""
        return self._http.request("football", "summary")

    def live_animation_schedule(self) -> Dict[str, Any]:
        """Get live animation schedule."""
        return self._http.request("football", "liveanimation/schedule")


class FootballAPI:
    """Football API aggregate - provides access to all football endpoints."""

    def __init__(self, http_client):
        self._http = http_client
        self.live_data = FootballLiveData(http_client)
        self.profile = FootballProfile(http_client)
        self.stats = FootballStats(http_client)
        self.odds = FootballOdds(http_client)
        self.common = FootballCommon(http_client)
