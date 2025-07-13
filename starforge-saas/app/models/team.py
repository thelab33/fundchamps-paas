from __future__ import annotations
from sqlalchemy.dialects.postgresql import JSONB
from app.extensions import db

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    team_name = db.Column(db.String(120), nullable=False)
    meta_description = db.Column(db.String(255), nullable=True)
    theme = db.Column(db.String(30), nullable=True)
    theme_color = db.Column(db.String(7), nullable=True)
    og_title = db.Column(db.String(120), nullable=True)
    og_description = db.Column(db.String(255), nullable=True)
    og_image = db.Column(db.String(255), nullable=True)
    hero_image = db.Column(db.String(255), nullable=True)
    favicon = db.Column(db.String(255), nullable=True)
    apple_icon = db.Column(db.String(255), nullable=True)
    custom_css = db.Column(db.String(255), nullable=True)
    body_class = db.Column(db.String(255), nullable=True)

    # Records: nested JSON for regional and national wins/losses
    record = db.Column(JSONB, nullable=False, default=lambda: {
        'regional': {'wins': 0, 'losses': 0},
        'national': {'wins': 0, 'losses': 0}
    })

    # Branding overrides
    lang_code = db.Column(db.String(5), default='en')

    def __repr__(self) -> str:
        return f"<Team {self.slug}: {self.team_name}>"
