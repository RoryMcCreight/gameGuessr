import logging
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import date
from game_logic import Game

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Enable CORS for all routes with specific origins
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

DATABASE = 'database/guessr.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This helps to return rows as dictionaries
    return conn

@app.route('/')
def index():
    return 'Welcome to the Guessr API!'

@app.route('/test-post', methods=['POST'])
def test_post():
    logging.debug("Test POST endpoint accessed")
    logging.debug(f"Request data: {request.json}")
    return jsonify({"message": "POST request received"})

@app.route('/daily-game', methods=['GET'])
def get_daily_game():
    logging.debug("Daily game endpoint accessed")
    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT game_id FROM DailyGames WHERE date = ?", (date.today().isoformat(),))
            result = cur.fetchone()
            if result:
                game_id = result['game_id']
                cur.execute("SELECT * FROM Games WHERE id = ?", (game_id,))
                game = cur.fetchone()
                logging.debug(f"Game found: {dict(game)}")
                return jsonify(dict(game))
            else:
                logging.debug("No game found for today")
                return jsonify({"error": "No game found for today"}), 404
    except Exception as e:
        logging.error(f"Error in /daily-game: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/guess', methods=['POST'])
def validate_guess():
    logging.debug("Guess endpoint accessed")
    data = request.json
    logging.debug(f"Request data: {data}")

    if not data or 'title' not in data:
        logging.error("Invalid request")
        return jsonify({"error": "Invalid request"}), 400

    guess_title = data.get('title')
    logging.debug(f"Guess title: {guess_title}")

    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Games WHERE title = ?", (guess_title,))
            guess = cur.fetchone()
            if not guess:
                logging.debug("Game not found")
                return jsonify({"error": "Game not found"}), 404

            current_date = date.today().isoformat()
            cur.execute("SELECT game_id FROM DailyGames WHERE date = ?", (current_date,))
            result = cur.fetchone()
            if result:
                daily_game_id = result['game_id']
                cur.execute("SELECT * FROM Games WHERE id = ?", (daily_game_id,))
                daily_game = cur.fetchone()

                clues = {
                    "release_year": guess['release_year'] == daily_game['release_year'],
                    "genre": guess['genre'] == daily_game['genre'],
                    "game_length": guess['game_length'] == daily_game['game_length'],
                    "publisher": guess['publisher'] == daily_game['publisher'],
                    "rating": guess['rating'] == daily_game['rating']
                }

                logging.debug(f"Clues: {clues}")
                return jsonify(clues)
            else:
                logging.debug("No daily game found")
                return jsonify({"error": "No daily game found"}), 404
    except Exception as e:
        logging.error(f"Error in /guess: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/games', methods=['GET'])
def get_games():
    logging.debug("Games endpoint accessed")
    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT title FROM Games")
            games = cur.fetchall()
            logging.debug(f"Games: {games}")
            return jsonify([dict(game) for game in games])
    except Exception as e:
        logging.error(f"Error in /api/games: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/new_game', methods=['POST'])
def new_game():
    logging.debug("New game endpoint accessed")
    global game
    try:
        game = Game()
        logging.debug("New game started")
        return jsonify({"message": "New game started"})
    except Exception as e:
        logging.error(f"Error in /new_game: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
