from flask import request, jsonify
from . import create_app, db
from .models import Game, DailyGame
from datetime import datetime

app = create_app()

@app.route('/games', methods=['GET'])
def get_games():
    games = Game.query.all()
    games_list = []
    for game in games:
        games_list.append({
            "title": game.title,
            "year": game.year,
            "genre": game.genre,
            "length": game.length,
            "publisher": game.publisher,
            "platform": game.platform,
            "developer": game.developer,
            "country": game.country,
            "rating": game.rating
        })
    return jsonify(games_list)

@app.route('/daily-game', methods=['GET'])
def get_daily_game():
    today = datetime.now().strftime('%Y-%m-%d')
    daily_game = DailyGame.query.filter_by(date=today).first()
    if daily_game:
        game = Game.query.get(daily_game.game_id)
        return jsonify({
            "title": game.title,
            "year": game.year,
            "genre": game.genre,
            "length": game.length,
            "publisher": game.publisher,
            "platform": game.platform,
            "developer": game.developer,
            "country": game.country,
            "rating": game.rating
        })
    else:
        return jsonify({"error": "No daily game found"}), 404
