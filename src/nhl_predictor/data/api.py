
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE_URL = "https://api-web.nhle.com/v1"


class NHLAPIClient:
    """Client for retrieving data from the NHL web API."""

    def __init__(self):
        self.session = requests.Session()

        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)

    def get_team_schedule(self, team: str, season: str) -> dict:
        """Fetch a team's schedule for a given NHL season."""

        url = (
            f"{BASE_URL}/club-schedule-season/"
            f"{team.upper()}/{season}"
        )

        response = self.session.get(url, timeout=30)
        response.raise_for_status()

        payload = response.json()

        if not isinstance(payload, dict):
            raise ValueError("Unexpected NHL API response format")

        if not isinstance(payload.get("games"), list):
            raise ValueError("NHL API response has no games list")

        return payload
