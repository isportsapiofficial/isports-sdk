"""
Tests for src/isports/basketball/__init__.py
"""
from unittest.mock import Mock
import pytest

from isports.basketball import (
    BasketballAPI,
    BasketballLiveData,
    BasketballProfile,
    BasketballStats,
    BasketballOdds,
    BasketballCommon,
)


@pytest.fixture
def mock_http():
    """Fixture providing a mocked HTTP client."""
    return Mock()


class TestBasketballLiveData:
    def test_livescores(self, mock_http):
        mock_http.request.return_value = {"code": 0, "data": []}
        api = BasketballLiveData(mock_http)
        result = api.livescores()
        mock_http.request.assert_called_once_with("basketball", "livescores")
        assert result == {"code": 0, "data": []}

    def test_livescore_changes(self, mock_http):
        mock_http.request.return_value = {"code": 0, "data": []}
        api = BasketballLiveData(mock_http)
        result = api.livescore_changes()
        mock_http.request.assert_called_once_with("basketball", "livescores/changes")
        assert result["code"] == 0

    def test_schedule_with_date(self, mock_http):
        mock_http.request.return_value = {"code": 0, "data": []}
        api = BasketballLiveData(mock_http)
        result = api.schedule(date="2024-01-15")
        mock_http.request.assert_called_once_with(
            "basketball", "schedule", {"date": "2024-01-15"}
        )

    def test_schedule_with_league_id(self, mock_http):
        api = BasketballLiveData(mock_http)
        api.schedule(league_id=123)
        mock_http.request.assert_called_once_with(
            "basketball", "schedule", {"leagueId": 123}
        )

    def test_schedule_with_match_id(self, mock_http):
        api = BasketballLiveData(mock_http)
        api.schedule(match_id=456)
        mock_http.request.assert_called_once_with(
            "basketball", "schedule", {"matchId": 456}
        )

    def test_schedule_basic_with_date(self, mock_http):
        api = BasketballLiveData(mock_http)
        api.schedule_basic(date="2024-01-15")
        mock_http.request.assert_called_once_with(
            "basketball", "schedule/basic", {"date": "2024-01-15"}
        )

    def test_lineups_without_params(self, mock_http):
        api = BasketballLiveData(mock_http)
        api.lineups()
        mock_http.request.assert_called_once_with("basketball", "lineups", {})

    def test_lineups_with_match_id(self, mock_http):
        api = BasketballLiveData(mock_http)
        api.lineups(match_id=789)
        mock_http.request.assert_called_once_with(
            "basketball", "lineups", {"matchId": 789}
        )

    def test_today_match(self, mock_http):
        api = BasketballLiveData(mock_http)
        api.today_match()
        mock_http.request.assert_called_once_with("basketball", "today/match")

    def test_livetext_list(self, mock_http):
        api = BasketballLiveData(mock_http)
        api.livetext_list()
        mock_http.request.assert_called_once_with("basketball", "livetext/list")

    def test_livetext(self, mock_http):
        api = BasketballLiveData(mock_http)
        api.livetext(match_id=100)
        mock_http.request.assert_called_once_with(
            "basketball", "livetext", {"matchId": 100}
        )


class TestBasketballProfile:
    def test_team_without_id(self, mock_http):
        api = BasketballProfile(mock_http)
        api.team()
        mock_http.request.assert_called_once_with("basketball", "team", {})

    def test_team_with_id(self, mock_http):
        api = BasketballProfile(mock_http)
        api.team(team_id=100)
        mock_http.request.assert_called_once_with(
            "basketball", "team", {"teamId": 100}
        )

    def test_team_search(self, mock_http):
        api = BasketballProfile(mock_http)
        api.team_search("Lakers")
        mock_http.request.assert_called_once_with(
            "basketball", "team/search", {"name": "Lakers"}
        )

    def test_player_without_id(self, mock_http):
        api = BasketballProfile(mock_http)
        api.player()
        mock_http.request.assert_called_once_with("basketball", "player", {})

    def test_player_with_id(self, mock_http):
        api = BasketballProfile(mock_http)
        api.player(player_id=200)
        mock_http.request.assert_called_once_with(
            "basketball", "player", {"playerId": 200}
        )

    def test_player_search(self, mock_http):
        api = BasketballProfile(mock_http)
        api.player_search("Jordan")
        mock_http.request.assert_called_once_with(
            "basketball", "player/search", {"name": "Jordan"}
        )

    def test_league(self, mock_http):
        api = BasketballProfile(mock_http)
        api.league()
        mock_http.request.assert_called_once_with("basketball", "league")

    def test_league_basic(self, mock_http):
        api = BasketballProfile(mock_http)
        api.league_basic()
        mock_http.request.assert_called_once_with("basketball", "league/basic")

    def test_cupqualify(self, mock_http):
        api = BasketballProfile(mock_http)
        api.cupqualify()
        mock_http.request.assert_called_once_with("basketball", "cupqualify")

    def test_playoffs(self, mock_http):
        api = BasketballProfile(mock_http)
        api.playoffs()
        mock_http.request.assert_called_once_with("basketball", "playoffs")

    def test_transfer_without_day(self, mock_http):
        api = BasketballProfile(mock_http)
        api.transfer()
        mock_http.request.assert_called_once_with("basketball", "transfer", {})

    def test_transfer_with_day(self, mock_http):
        api = BasketballProfile(mock_http)
        api.transfer(day=7)
        mock_http.request.assert_called_once_with(
            "basketball", "transfer", {"day": 7}
        )


class TestBasketballStats:
    def test_standing(self, mock_http):
        api = BasketballStats(mock_http)
        api.standing(league_id="39")
        mock_http.request.assert_called_once_with(
            "basketball", "standing/league", {"leagueId": "39"}
        )

    def test_cup_standing(self, mock_http):
        api = BasketballStats(mock_http)
        api.cup_standing(league_id="50")
        mock_http.request.assert_called_once_with(
            "basketball", "standing/cup", {"leagueId": "50"}
        )

    def test_stats_with_match_id(self, mock_http):
        api = BasketballStats(mock_http)
        api.stats(match_id=300)
        mock_http.request.assert_called_once_with(
            "basketball", "stats", {"matchId": 300}
        )

    def test_stats_with_date(self, mock_http):
        api = BasketballStats(mock_http)
        api.stats(date="2024-01-15")
        mock_http.request.assert_called_once_with(
            "basketball", "stats", {"date": "2024-01-15"}
        )

    def test_quarters_stats(self, mock_http):
        api = BasketballStats(mock_http)
        api.quarters_stats()
        mock_http.request.assert_called_once_with("basketball", "stats", {"cmd": "stats"})

    def test_quarters_stats_with_match_id_and_date(self, mock_http):
        api = BasketballStats(mock_http)
        api.quarters_stats(match_id=100, date="2026-04-20")
        mock_http.request.assert_called_once_with(
            "basketball", "stats", {"cmd": "stats", "matchId": 100, "date": "2026-04-20"}
        )

    def test_analysis(self, mock_http):
        api = BasketballStats(mock_http)
        api.analysis(match_id=12345)
        mock_http.request.assert_called_once_with(
            "basketball", "analysis", {"matchId": 12345}
        )


class TestBasketballOdds:
    def test_fulltime(self, mock_http):
        api = BasketballOdds(mock_http)
        api.fulltime(match_id=100)
        mock_http.request.assert_called_once_with(
            "basketball", "odds/fulltime", {"matchId": 100}
        )

    def test_fulltime_changes(self, mock_http):
        api = BasketballOdds(mock_http)
        api.fulltime_changes(league_id=10)
        mock_http.request.assert_called_once_with(
            "basketball", "odds/fulltime/changes", {"leagueId": 10}
        )

    def test_half(self, mock_http):
        api = BasketballOdds(mock_http)
        api.half()
        mock_http.request.assert_called_once_with("basketball", "odds/half", {})

    def test_quarter(self, mock_http):
        api = BasketballOdds(mock_http)
        api.quarter(match_id=200)
        mock_http.request.assert_called_once_with(
            "basketball", "odds/quarter", {"matchId": 200}
        )

    def test_history(self, mock_http):
        api = BasketballOdds(mock_http)
        api.history(league_id=5)
        mock_http.request.assert_called_once_with(
            "basketball", "odds/history", {"leagueId": 5}
        )

    def test_european_all(self, mock_http):
        api = BasketballOdds(mock_http)
        api.european_all(match_id=300)
        mock_http.request.assert_called_once_with(
            "basketball", "odds/european/all", {"matchId": 300}
        )

    def test_inplay(self, mock_http):
        api = BasketballOdds(mock_http)
        api.inplay()
        mock_http.request.assert_called_once_with("basketball", "odds/inplay", {})


class TestBasketballCommon:
    def test_country(self, mock_http):
        api = BasketballCommon(mock_http)
        api.country()
        mock_http.request.assert_called_once_with("basketball", "country")

    def test_bookmaker(self, mock_http):
        api = BasketballCommon(mock_http)
        api.bookmaker()
        mock_http.request.assert_called_once_with("basketball", "bookmaker")

    def test_schedule_modify(self, mock_http):
        api = BasketballCommon(mock_http)
        api.schedule_modify()
        mock_http.request.assert_called_once_with("basketball", "schedule/modify")


class TestBasketballAPI:
    def test_initialization(self, mock_http):
        api = BasketballAPI(mock_http)
        assert api._http is mock_http
        assert isinstance(api.live_data, BasketballLiveData)
        assert isinstance(api.profile, BasketballProfile)
        assert isinstance(api.stats, BasketballStats)
        assert isinstance(api.odds, BasketballOdds)
        assert isinstance(api.common, BasketballCommon)
