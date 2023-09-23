from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from main import db

# TVGenre Model
class TVGenre(db.Model):
    __tablename__ = 'tv_genres'
    id = db.Column(db.Integer, primary_key=True)

    tv_show_id = db.Column(db.Integer, ForeignKey('tv_shows.id'), nullable=False)
    genre_id = db.Column(db.Integer, ForeignKey('genres.id'), nullable=False)

    # Relationships
    tv_show = relationship('TVShow', back_populates='tv_genres')
    genre = relationship('Genre', back_populates='tv_genres')