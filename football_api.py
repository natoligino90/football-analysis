import requests
from datetime import datetime, timedelta

class FootballDataAPI:
    def __init__(self, api_key):
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {'X-Auth-Token': api_key}
    
    def get_upcoming_matches(self, competition_code='SA', days_ahead=7):
        date_to = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        url = f"{self.base_url}/competitions/{competition_code}/matches"
        params = {'status': 'SCHEDULED', 'dateTo': date_to}
        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
