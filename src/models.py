from . import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    platform = db.Column(db.String, nullable=False)
    developer = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)

class DailyGame(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    date = db.Column(db.String, nullable=False, unique=True)
