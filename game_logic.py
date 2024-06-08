import random
import sqlite3
from datetime import date

CATEGORIES = ["title", "year", "genre", "length", "publisher", "platform", "developer", "country", "rating"]

DATABASE = 'database/guessr.db'  # Adjust the path if necessary

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def get_daily_game_from_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT game_id FROM DailyGames WHERE date = ?", (date.today().isoformat(),))
    result = cur.fetchone()
    if result:
        game_id = result[0]
        cur.execute("SELECT * FROM Games WHERE id = ?", (game_id,))
        game = cur.fetchone()
        conn.close()
        return game
    else:
        conn.close()
        return None

class Game:
    def __init__(self):
        self.answer = get_daily_game_from_db()
        self.guesses = []
        self.max_guesses = 10

    def make_guess(self, guess):
        self.guesses.append(guess)
        feedback = self.get_feedback(guess)
        return feedback

    def get_feedback(self, guess):
        feedback = {}
        for category in CATEGORIES:
            if category in ['title', 'developer', 'publisher', 'platform', 'country']:
                feedback[category] = guess[category] == self.answer[CATEGORIES.index(category)]
            elif category in ['year', 'length', 'rating']:
                feedback[category] = self._get_proximity_feedback(guess[category], self.answer[CATEGORIES.index(category)], category)
            else:
                feedback[category] = guess[category] == self.answer[CATEGORIES.index(category)]
        return feedback

    def _get_proximity_feedback(self, guess_value, answer_value, category):
        if guess_value == answer_value:
            return "Exact"
        elif guess_value > answer_value:
            return "Later" if category == 'year' else "Longer"
        else:
            return "Earlier" if category == 'year' else "Shorter"

    def is_game_over(self):
        return len(self.guesses) >= self.max_guesses or all(self.guesses[-1][category] == self.answer[CATEGORIES.index(category)] for category in CATEGORIES)

    def get_answer(self):
        return self.answer if self.is_game_over() else None
