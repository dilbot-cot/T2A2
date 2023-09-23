from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from main import db

# MovieGenre Model
class MovieGenre(db.Model):
    __tablename__ = 'movie_genres'
    id = db.Column(db.Integer, primary_key=True)

    movie_id = db.Column(db.Integer, ForeignKey('movies.id'), nullable=False)
    genre_id = db.Column(db.Integer, ForeignKey('genres.id'), nullable=False)

    # Relationships
    movie = relationship('Movie', back_populates='movie_genres')
    genre = relationship('Genre', back_populates='movie_genres')