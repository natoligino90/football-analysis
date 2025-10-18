from flask import Flask, jsonify, render_template, request
from football_api import FootballDataAPI, PatternAnalyzer
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = '9459832e421b4e4e93730bdf969514ff'
api_client = FootballDataAPI(API_KEY)
analyzer = PatternAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/palinsesto')
def get_palinsesto():
    competition = request.args.get('competition', 'SA')
    days = int(request.args.get('days', 7))
    
    try:
        data = api_client.get_upcoming_matches(competition, days)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
