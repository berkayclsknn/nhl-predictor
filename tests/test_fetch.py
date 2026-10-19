
from nhl_predictor.data.fetch import parse_completed_games


def make_game(game_id, home_score, away_score, state="OFF"):
    return {
        "id": game_id,
        "season": 20232024,
        "gameDate": "2023-11-10",
        "gameType": 2,
        "gameState": state,
        "homeTeam": {
            "abbrev": "OTT",
            "score": home_score,
        },
        "awayTeam": {
            "abbrev": "MTL",
            "score": away_score,
        },
    }


def test_home_win():
    payload = {
        "games": [make_game(1, 4, 2)]
    }

    df = parse_completed_games(payload)

    assert len(df) == 1
    assert df.iloc[0]["home_win"] == 1


def test_away_win():
    payload = {
        "games": [make_game(2, 1, 3)]
    }

    df = parse_completed_games(payload)

    assert df.iloc[0]["home_win"] == 0


def test_skip_unfinished_games():
    payload = {
        "games": [make_game(3, 0, 0, state="FUT")]
    }

    df = parse_completed_games(payload)

    assert df.empty
