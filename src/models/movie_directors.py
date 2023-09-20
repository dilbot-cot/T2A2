from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from main import db

# MovieDirector Model
class MovieDirector(db.Model):
    __tablename__ = 'movie_directors'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, ForeignKey('movies.id'), nullable=False)
    director_id = db.Column(db.Integer, ForeignKey('directors.id'), nullable=False)

    # Relationships
    movie = relationship('Movie', back_populates='movie_directors')
    director = relationship('Director', back_populates='movie_directors')