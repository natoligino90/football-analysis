from flask import Flask, jsonify, render_template, request
from football_api import FootballDataAPI, PatternAnalyzer
from football_api_apisports import APIFootballAPIClient
import os
from datetime import datetime

app = Flask(__name__)

# Prima API: Football-Data.org
API_KEY = os.getenv('FOOTBALL_DATA_API_KEY') or '9459832e421b4e4e93730bdf969514ff'
api_client = FootballDataAPI(API_KEY)
analyzer = PatternAnalyzer()

# Seconda API: API-Football (api-sports)
API_KEY_APISPORTS = os.getenv('API_FOOTBALL_KEY') or '8a07306b432145e4d1465338c94a0539'
api_sports_client = APIFootballAPIClient(API_KEY_APISPORTS)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/palinsesto')
def get_palinsesto():
    competition = request.args.get('competition', 'SA')
    days = int(request.args.get('days', 7))
    try:
        matches_data = api_client.get_upcoming_matches(competition, days, limit=8)
        return jsonify({'success': True, 'data': matches_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/probabilita_pareggio')
def probabilita_pareggio():
    competition = request.args.get('competition', 'SA')
    days = int(request.args.get('days', 7))
    try:
        matches_data = api_client.get_upcoming_matches(competition, days, limit=8)
        prob_list = analyzer.estimate_draw_probability(matches_data, api_client)
        out = []
        for item in prob_list:
            m = item['match']
            out.append({
