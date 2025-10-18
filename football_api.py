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

class PatternAnalyzer:
    @staticmethod
    def find_draw_patterns(matches_data):
        patterns = {'0-0': [], '1-1': [], '2-2': [], '3-3': []}
        for match in matches_data.get('matches', []):
            score = match.get('score', {}).get('fullTime', {})
            home = score.get('home')
            away = score.get('away')
            if home is not None and away is not None and home == away:
                pattern_key = f"{home}-{away}"
                if pattern_key in patterns:
                    patterns[pattern_key].append(match)
        return patterns
