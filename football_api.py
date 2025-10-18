import requests
from datetime import datetime, timedelta

class FootballDataAPI:
    def __init__(self, api_key):
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {'X-Auth-Token': api_key}
    
    def get_upcoming_matches(self, competition_code='SA', days_ahead=7, limit=8):
        date_to = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        url = f"{self.base_url}/competitions/{competition_code}/matches"
        params = {'status': 'SCHEDULED', 'dateTo': date_to}
        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        match_list = data.get('matches', [])[:limit]
        data['matches'] = match_list
        return data
    
    def get_team_past_results(self, team_id, n=3):
        url = f"{self.base_url}/teams/{team_id}/matches"
        params = {'status': 'FINISHED', 'limit': n}
        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

class PatternAnalyzer:
    @staticmethod
    def estimate_draw_probability(matches_data, api_client):
        probabilities = []
        for match in matches_data.get('matches', []):
            home_id = match['homeTeam']['id']
            away_id = match['awayTeam']['id']
            home_results = api_client.get_team_past_results(home_id, n=3)
            away_results = api_client.get_team_past_results(away_id, n=3)

            def calc_draw_percent(results):
                draws = 0
                total = 0
                for m in results.get('matches', []):
                    score = m.get('score', {}).get('fullTime', {})
                    home = score.get('home')
                    away = score.get('away')
                    if home is not None and away is not None and home == away:
                        draws += 1
                    total += 1
                return draws/total if total else 0

            home_draw = calc_draw_percent(home_results)
            away_draw = calc_draw_percent(away_results)
            prob = round(((home_draw + away_draw) / 2) * 100, 1)
            probabilities.append({'match': match, 'draw_probability': prob})
        return probabilities
