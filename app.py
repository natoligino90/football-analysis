@app.route('/api/probabilita_pareggio')
def probabilita_pareggio():
    competition = request.args.get('competition', 'SA')
    days = int(request.args.get('days', 7))
    try:
        matches_data = api_client.get_upcoming_matches(competition, days)
        prob_list = analyzer.estimate_draw_probability(matches_data, api_client)
        # Da qui ritorniamo solo le info semplificate
        out = []
        for item in prob_list:
            m = item['match']
            out.append({
                'date': m['utcDate'],
                'competition': m['competition']['name'] if 'competition' in m else '',
                'home': m['homeTeam']['name'],
                'away': m['awayTeam']['name'],
                'draw_probability': item['draw_probability']
            })
        return jsonify({'success': True, 'data': out})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
