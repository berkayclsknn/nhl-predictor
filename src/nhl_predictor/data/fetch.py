
import json
from pathlib import Path

import pandas as pd

from nhl_predictor.data.api import NHLAPIClient


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

COLUMNS = [
    "game_id",
    "season",
    "date",
    "home_team",
    "away_team",
    "home_goals",
    "away_goals",
    "home_win",
]


def parse_completed_games(payload: dict) -> pd.DataFrame:
    """Transform NHL schedule JSON into completed game rows."""

    rows = []

    for game in payload["games"]:
        # 2 = NHL regular-season game
        if game.get("gameType") != 2:
            continue

        # OFF indicates a completed game.
        if game.get("gameState") != "OFF":
            continue

        home = game["homeTeam"]
        away = game["awayTeam"]

        home_goals = home.get("score")
        away_goals = away.get("score")

        if home_goals is None or away_goals is None:
            continue

        rows.append({
            "game_id": game["id"],
            "season": game["season"],
            "date": game["gameDate"],
            "home_team": home["abbrev"],
            "away_team": away["abbrev"],
            "home_goals": home_goals,
            "away_goals": away_goals,
            "home_win": int(home_goals > away_goals),
        })

    return pd.DataFrame(rows, columns=COLUMNS)


def main():
    team = "OTT"
    season = "20232024"

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    client = NHLAPIClient()

    print(f"Fetching {team} schedule for {season}...")
    payload = client.get_team_schedule(team, season)

    raw_path = RAW_DIR / f"{team}_{season}.json"

    with raw_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)

    games = parse_completed_games(payload)

    if games.empty:
        raise ValueError("No completed games were found.")

    games = games.sort_values(["date", "game_id"])
    games = games.drop_duplicates(subset=["game_id"])

    output_path = PROCESSED_DIR / f"{team}_{season}.csv"
    games.to_csv(output_path, index=False)

    print(f"Saved {len(games)} completed games.")
    print(f"Dataset: {output_path}")
    print(games.head().to_string(index=False))


if __name__ == "__main__":
    main()
