from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import relationship
from main import db

# Movie Model
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    release_date = db.Column(Date, nullable=False)

    # Relationships
    movie_genre = relationship('MovieGenre', back_populates='movie')
    reviews = relationship('Review', back_populates='movie')
    movie_actors = relationship('MovieActor', back_populates='movie')
    movie_directors = relationship('MovieDirector', back_populates='movie')
