from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import date
from game_logic import Game, get_daily_game_from_db  # Import the Game class and get_daily_game_from_db function

app = Flask(__name__)

DATABASE = 'database/guessr.db'  # Adjust the path if necessary

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# Initialize game instance
game = Game()

@app.route('/test-post', methods=['POST'])
def test_post():
    return jsonify({"message": "POST request received"})

@app.route('/daily-game', methods=['GET'])
def get_daily_game():
    print("Daily game endpoint accessed")
    game_data = get_daily_game_from_db()
    if game_data:
        return jsonify(game_data)
    else:
        return jsonify({"error": "No game found for today"}), 404

@app.route('/guess', methods=['POST'])
def validate_guess():
    print("Guess endpoint accessed")
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    guess_title = data.get('title')
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Games WHERE title = ?", (guess_title,))
    guess = cur.fetchone()
    
    if not guess:
        conn.close()
        return jsonify({"error": "Game not found"}), 404

    current_date = date.today().isoformat()
    
    cur.execute("SELECT game_id FROM DailyGames WHERE date = ?", (current_date,))
    result = cur.fetchone()
    if result:
        daily_game_id = result[0]
        cur.execute("SELECT * FROM Games WHERE id = ?", (daily_game_id,))
        daily_game = cur.fetchone()
        
        clues = {
            "year_of_release": guess[2] == daily_game[2],
            "genre": guess[3] == daily_game[3],
            "average_length_to_complete": guess[4] == daily_game[4],
            "publisher": guess[5] == daily_game[5],
            "average_user_rating": guess[6] == daily_game[6]
        }

        conn.close()
        return jsonify(clues)
    else:
        conn.close()
        return jsonify({"error": "No daily game found"}), 404

@app.route('/games', methods=['GET'])
def get_games():
    print("Games endpoint accessed")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Games")
    games = cur.fetchall()
    conn.close()
    return jsonify(games)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Guessr API!"

@app.route('/new_game', methods=['POST'])
def new_game():
    global game
    game = Game()
    return jsonify({"message": "New game started"})

@app.route('/play', methods=['GET'])
def play():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
