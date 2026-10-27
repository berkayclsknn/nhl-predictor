
import pandas as pd


def build_ottawa_features(games: pd.DataFrame) -> pd.DataFrame:

    df = games.copy()

    # Always process games chronologically.
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["date", "game_id"]).reset_index(drop=True)

    # Express each game from Ottawa's perspective.
    df["is_home"] = (df["home_team"] == "OTT").astype(int)

    df["ottawa_win"] = df.apply(
        lambda row: row["home_win"]
        if row["is_home"] == 1
        else 1 - row["home_win"],
        axis=1,
    )

    df["goals_for"] = df["home_goals"].where(
        df["is_home"] == 1, df["away_goals"]
    )

    df["goals_against"] = df["away_goals"].where(
        df["is_home"] == 1, df["home_goals"]
    )

    # Number of full days between games.
    df["rest_days"] = (
        df["date"].diff().dt.days - 1
    ).clip(lower=0)

    # CRITICAL: shift(1) excludes the current game's result.
    df["last_5_win_rate"] = (
        df["ottawa_win"]
        .shift(1)
        .rolling(window=5, min_periods=5)
        .mean()
    )

    df["last_5_goals_for"] = (
        df["goals_for"]
        .shift(1)
        .rolling(window=5, min_periods=5)
        .mean()
    )

    df["last_5_goals_against"] = (
        df["goals_against"]
        .shift(1)
        .rolling(window=5, min_periods=5)
        .mean()
    )

    feature_columns = [
        "is_home",
        "rest_days",
        "last_5_win_rate",
        "last_5_goals_for",
        "last_5_goals_against",
    ]

    # Games without sufficient prior history aren't used yet.
    df = df.dropna(subset=feature_columns).copy()

    return df
