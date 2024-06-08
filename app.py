import os
from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
import sqlite3

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

DATABASE = 'database/guessr.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# Configure OAuth
oauth = OAuth(app)
igdb = oauth.register(
    'igdb',
    client_id=os.environ.get('IGDB_CLIENT_ID'),  # Use environment variables
    client_secret=os.environ.get('IGDB_CLIENT_SECRET'),  # Use environment variables
    authorize_url='https://id.twitch.tv/oauth2/authorize',
    authorize_params=None,
    access_token_url='https://id.twitch.tv/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'user:read:email'},
)

@app.route('/')
def index():
    return 'Welcome to the Guessr API!'

@app.route('/login')
def login():
    redirect_uri = url_for('authorized', _external=True)
    return igdb.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('igdb_token')
    return redirect(url_for('index'))

@app.route('/callback')
def authorized():
    token = igdb.authorize_access_token()
    if not token:
        return 'Access denied'
    session['igdb_token'] = token
    return redirect(url_for('index'))

@oauth.tokengetter
def get_igdb_oauth_token():
    return session.get('igdb_token')

@app.route('/test-post', methods=['POST'])
def test_post():
    return jsonify({"message": "POST request received"})

@app.route('/daily-game', methods=['GET'])
def get_daily_game():
    print("Daily game endpoint accessed")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT game_id FROM DailyGames WHERE date = ?", (date.today().isoformat(),))
    result = cur.fetchone()
    if result:
        game_id = result[0]
        cur.execute("SELECT * FROM Games WHERE id = ?", (game_id,))
        game = cur.fetchone()
        conn.close()
        return jsonify(game)
    else:
        conn.close()
        return jsonify({"error": "No game found for today"}), 404

@app.route('/guess', methods=['POST'])
def validate_guess():
    print("Guess endpoint accessed")
    print("Request method:", request.method)
    print("Request content type:", request.content_type)
    print("Request headers:", request.headers)
    print("Request JSON body:", request.json)
    
    data = request.json
    if not data or 'title' not in data:
        print("Invalid request")
        return jsonify({"error": "Invalid request"}), 400
    
    guess_title = data.get('title')
    print(f"Guess title: {guess_title}")
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Games WHERE title = ?", (guess_title,))
    guess = cur.fetchone()
    
    if not guess:
        print("Game not found")
        conn.close()
        return jsonify({"error": "Game not found"}), 404

    current_date = date.today().isoformat()
    print(f"Current date: {current_date}")
    
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
        print("Returning clues")
        return jsonify(clues)
    else:
        print("No daily game found")
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

@app.route('/new_game', methods=['POST'])
def new_game():
    global game
    game = Game()
    return jsonify({"message": "New game started"})

@app.route('/play', methods=['GET'])
def play():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
