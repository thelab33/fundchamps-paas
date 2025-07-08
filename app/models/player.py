# app/models/player.py
from app import db

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    team = db.Column(db.String(100))
    bio = db.Column(db.Text)  # Add a bio or mission description for each player

    def __repr__(self):
        return f'<Player {self.name}>'
