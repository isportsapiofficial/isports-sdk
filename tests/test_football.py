"""
Tests for iSports SDK Football API endpoints.
"""

import pytest
from unittest.mock import patch, MagicMock

from isports import ISportsClient
from isports.exceptions import AuthenticationError


class TestFootballLiveData:
    """Test Football Live Data endpoints."""

    def setup_method(self):
        self.client = ISportsClient(api_key="test_key")

    @patch("isports.http._HTTPClient.request")
    def test_livescores(self, mock_request):
        mock_request.return_value = {"code": 0, "data": [{"matchId": 1}]}
        result = self.client.football.live_data.livescores()
        mock_request.assert_called_once_with("football", "livescores")
        assert result["data"][0]["matchId"] == 1

    @patch("isports.http._HTTPClient.request")
    def test_livescore_changes(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        result = self.client.football.live_data.livescore_changes()
        mock_request.assert_called_once_with("football", "livescores/changes")
        assert result["code"] == 0

    @patch("isports.http._HTTPClient.request")
    def test_schedule_basic_with_date(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.schedule_basic(date="2024-01-15")
        mock_request.assert_called_once_with(
            "football", "schedule/basic", {"date": "2024-01-15"}
        )

    @patch("isports.http._HTTPClient.request")
    def test_schedule_basic_with_league_id_and_season(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.schedule_basic(league_id="39", season="2024-2025")
        mock_request.assert_called_once_with(
            "football", "schedule/basic", {"leagueId": "39", "season": "2024-2025"}
        )

    @patch("isports.http._HTTPClient.request")
    def test_schedule_basic_with_match_id(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.schedule_basic(match_id="12345")
        mock_request.assert_called_once_with(
            "football", "schedule/basic", {"matchId": "12345"}
        )

    @patch("isports.http._HTTPClient.request")
    def test_schedule(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.schedule(
            date="2024-01-15",
            league_id="39",
            season="2024-2025",
            sub_league_id="1",
            stage_id="2",
            match_id="12345",
        )
        mock_request.assert_called_once_with(
            "football", "schedule",
            {
                "date": "2024-01-15",
                "leagueId": "39",
                "season": "2024-2025",
                "subLeagueId": "1",
                "stageId": "2",
                "matchId": "12345",
            }
        )

    @patch("isports.http._HTTPClient.request")
    def test_events_without_params(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.events()
        mock_request.assert_called_once_with("football", "events", {})

    @patch("isports.http._HTTPClient.request")
    def test_events_with_date(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.events(date="2026-04-25")
        mock_request.assert_called_once_with(
            "football", "events", {"date": "2026-04-25"}
        )

    @patch("isports.http._HTTPClient.request")
    def test_events_with_cmd(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.events(cmd=True)
        mock_request.assert_called_once_with(
            "football", "events", {"cmd": "new"}
        )

    @patch("isports.http._HTTPClient.request")
    def test_events_corner(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.events_corner()
        mock_request.assert_called_once_with("football", "events/corner")

    @patch("isports.http._HTTPClient.request")
    def test_lineups_with_match_id(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.lineups(match_id="12345")
        mock_request.assert_called_once_with(
            "football", "lineups", {"matchId": "12345"}
        )

    @patch("isports.http._HTTPClient.request")
    def test_lineups_with_preview(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.lineups(match_id="12345", is_preview=True)
        mock_request.assert_called_once_with(
            "football", "lineups", {"matchId": "12345", "isPreview": "true"}
        )

    @patch("isports.http._HTTPClient.request")
    def test_injury(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.injury()
        mock_request.assert_called_once_with("football", "injury")

    @patch("isports.http._HTTPClient.request")
    def test_livetext_list(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.livetext_list()
        mock_request.assert_called_once_with("football", "livetext/list")

    @patch("isports.http._HTTPClient.request")
    def test_livetext(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.live_data.livetext(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "livetext", {"matchId": 12345}
        )


class TestFootballProfile:
    """Test Football Profile endpoints."""

    def setup_method(self):
        self.client = ISportsClient(api_key="test_key")

    @patch("isports.http._HTTPClient.request")
    def test_league_basic(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.league_basic()
        mock_request.assert_called_once_with("football", "league/basic")

    @patch("isports.http._HTTPClient.request")
    def test_league(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.league()
        mock_request.assert_called_once_with("football", "league")

    @patch("isports.http._HTTPClient.request")
    def test_league_sub(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.league_sub()
        mock_request.assert_called_once_with("football", "league/sub")

    @patch("isports.http._HTTPClient.request")
    def test_league_stage(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.league_stage()
        mock_request.assert_called_once_with("football", "league/stage")

    @patch("isports.http._HTTPClient.request")
    def test_team_all(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.team()
        mock_request.assert_called_once_with("football", "team", {})

    @patch("isports.http._HTTPClient.request")
    def test_team_by_id(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.team(team_id=33)
        mock_request.assert_called_once_with(
            "football", "team", {"teamId": 33}
        )

    @patch("isports.http._HTTPClient.request")
    def test_team_search(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.team_search("Manchester")
        mock_request.assert_called_once_with(
            "football", "team/search", {"name": "Manchester"}
        )

    @patch("isports.http._HTTPClient.request")
    def test_player_by_team(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.player(team_id=33)
        mock_request.assert_called_once_with(
            "football", "player", {"teamId": 33}
        )

    @patch("isports.http._HTTPClient.request")
    def test_player_by_day(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.player(day="2024-01-15")
        mock_request.assert_called_once_with(
            "football", "player", {"day": "2024-01-15"}
        )

    @patch("isports.http._HTTPClient.request")
    def test_player_by_id(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.player(player_id=1234)
        mock_request.assert_called_once_with(
            "football", "player", {"playerId": 1234}
        )

    @patch("isports.http._HTTPClient.request")
    def test_player_search(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.player_search("Ronaldo")
        mock_request.assert_called_once_with(
            "football", "player/search", {"name": "Ronaldo"}
        )

    @patch("isports.http._HTTPClient.request")
    def test_referee(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.referee()
        mock_request.assert_called_once_with("football", "referee")

    @patch("isports.http._HTTPClient.request")
    def test_transfer(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.profile.transfer(league_id=39)
        mock_request.assert_called_once_with(
            "football", "transfer", {"leagueId": 39}
        )


class TestFootballStats:
    """Test Football Statistics endpoints."""

    def setup_method(self):
        self.client = ISportsClient(api_key="test_key")

    @patch("isports.http._HTTPClient.request")
    def test_standing_with_league(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.stats.standing(league_id=39)
        mock_request.assert_called_once_with(
            "football", "standing/league", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_standing_without_params(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.stats.standing()
        mock_request.assert_called_once_with("football", "standing/league", {})

    @patch("isports.http._HTTPClient.request")
    def test_cup_standing(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.stats.cup_standing(cup_id=2)
        mock_request.assert_called_once_with(
            "football", "standing/cup", {"cupId": 2}
        )

    @patch("isports.http._HTTPClient.request")
    def test_subleague_standing(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.stats.subleague_standing(league_id=39)
        mock_request.assert_called_once_with(
            "football", "standing/league/getsub", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_topscorer(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.stats.topscorer(league_id=39)
        mock_request.assert_called_once_with(
            "football", "topscorer", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_analysis(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.stats.analysis(match_id=12345)
        mock_request.assert_called_once_with("football", "analysis", {"matchId": 12345})

    @patch("isports.http._HTTPClient.request")
    def test_playerstats_match_list(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.stats.playerstats_match_list()
        mock_request.assert_called_once_with("football", "playerstats/match/list")

    @patch("isports.http._HTTPClient.request")
    def test_playerstats_match(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.stats.playerstats_match(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "playerstats/match", {"matchId": 12345}
        )

    @patch("isports.http._HTTPClient.request")
    def test_playerstats_league_list(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.stats.playerstats_league_list()
        mock_request.assert_called_once_with("football", "playerstats/league/list")

    @patch("isports.http._HTTPClient.request")
    def test_playerstats_league(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.stats.playerstats_league(league_id=39)
        mock_request.assert_called_once_with(
            "football", "playerstats/league", {"leagueId": 39}
        )


class TestFootballOdds:
    """Test Football Odds endpoints."""

    def setup_method(self):
        self.client = ISportsClient(api_key="test_key")

    @patch("isports.http._HTTPClient.request")
    def test_main(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.main(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "odds/main", {"matchId": 12345}
        )

    @patch("isports.http._HTTPClient.request")
    def test_main_changes(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.main_changes(league_id=39)
        mock_request.assert_called_once_with(
            "football", "odds/main/changes", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_main_future(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.main_future(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "odds/main/future", {"matchId": 12345}
        )

    @patch("isports.http._HTTPClient.request")
    def test_main_history(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.main_history(league_id=39)
        mock_request.assert_called_once_with(
            "football", "odds/main/history", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_all_odds(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.all_odds(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "odds/all", {"matchId": 12345}
        )

    @patch("isports.http._HTTPClient.request")
    def test_all_changes(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.all_changes(league_id=39)
        mock_request.assert_called_once_with(
            "football", "odds/all/changes", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_all_future(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.all_future(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "odds/all/future", {"matchId": 12345}
        )

    @patch("isports.http._HTTPClient.request")
    def test_all_history(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.all_history(league_id=39)
        mock_request.assert_called_once_with(
            "football", "odds/all/history", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_inplay(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.inplay(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "odds/inplay", {"matchId": 12345}
        )

    @patch("isports.http._HTTPClient.request")
    def test_inplay_half(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.inplay_half(league_id=39)
        mock_request.assert_called_once_with(
            "football", "odds/inplay/half", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_european_all(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.european_all(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "odds/european/all", {"matchId": 12345}
        )

    @patch("isports.http._HTTPClient.request")
    def test_european_half(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.european_half(league_id=39)
        mock_request.assert_called_once_with(
            "football", "odds/european/half", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_odds_by_id(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.odds_by_id(match_id=12345, company_id=3)
        mock_request.assert_called_once_with(
            "football", "odds/oddsbyid", {"matchId": 12345, "companyID": 3}
        )

    @patch("isports.http._HTTPClient.request")
    def test_outrights(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.outrights(league_id=39)
        mock_request.assert_called_once_with(
            "football", "odds/outrights", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_halffull_prematch(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.halffull_prematch(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "odds/halffull/prematch", {"matchId": 12345}
        )

    @patch("isports.http._HTTPClient.request")
    def test_halffull_inplay(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.halffull_inplay(league_id=39)
        mock_request.assert_called_once_with(
            "football", "odds/halffull/inplay", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_cornerstotal_prematch(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.cornerstotal_prematch(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "odds/cornerstotal/prematch", {"matchId": 12345}
        )

    @patch("isports.http._HTTPClient.request")
    def test_cornerstotal_inplay(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.cornerstotal_inplay(league_id=39)
        mock_request.assert_called_once_with(
            "football", "odds/cornerstotal/inplay", {"leagueId": 39}
        )

    @patch("isports.http._HTTPClient.request")
    def test_betfair(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.odds.betfair(match_id=12345)
        mock_request.assert_called_once_with(
            "football", "betfair", {"matchId": 12345}
        )


class TestFootballCommon:
    """Test Football Common endpoints."""

    def setup_method(self):
        self.client = ISportsClient(api_key="test_key")

    @patch("isports.http._HTTPClient.request")
    def test_team_modify(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.common.team_modify()
        mock_request.assert_called_once_with("football", "team/modify")

    @patch("isports.http._HTTPClient.request")
    def test_player_modify(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.common.player_modify()
        mock_request.assert_called_once_with("football", "player/modify")

    @patch("isports.http._HTTPClient.request")
    def test_schedule_modify(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.common.schedule_modify()
        mock_request.assert_called_once_with("football", "schedule/modify")

    @patch("isports.http._HTTPClient.request")
    def test_country(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.common.country()
        mock_request.assert_called_once_with("football", "country")

    @patch("isports.http._HTTPClient.request")
    def test_bookmaker(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.common.bookmaker()
        mock_request.assert_called_once_with("football", "bookmaker")

    @patch("isports.http._HTTPClient.request")
    def test_fifaranking(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.common.fifaranking()
        mock_request.assert_called_once_with("football", "fifaranking")

    @patch("isports.http._HTTPClient.request")
    def test_summary(self, mock_request):
        mock_request.return_value = {"code": 0, "data": []}
        self.client.football.common.summary()
        mock_request.assert_called_once_with("football", "summary")
