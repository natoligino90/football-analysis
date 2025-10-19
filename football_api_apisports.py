import requests

class APIFootballAPIClient:
    def __init__(self, api_key):
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {'x-apisports-key': api_key}

    def get_fixtures(self, league_id, date):
        url = f"{self.base_url}/fixtures"
        params = {'league': league_id, 'date': date}
        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
