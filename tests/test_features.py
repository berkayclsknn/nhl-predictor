
import pandas as pd

from nhl_predictor.features.build_features import (
    build_ottawa_features,
)


def test_current_game_result_does_not_change_features():
    games = pd.read_csv("data/processed/OTT_20232024.csv")

    original = build_ottawa_features(games)

    modified = games.copy()

    # Change only the final game's outcome.
    last = modified.index[-1]
    modified.loc[last, "home_goals"] = 20
    modified.loc[last, "away_goals"] = 0
    modified.loc[last, "home_win"] = 1

    changed = build_ottawa_features(modified)

    features = [
        "is_home",
        "rest_days",
        "last_5_win_rate",
        "last_5_goals_for",
        "last_5_goals_against",
    ]

    pd.testing.assert_series_equal(
        original.iloc[-1][features],
        changed.iloc[-1][features],
    )
