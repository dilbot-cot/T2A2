from main import db
from .join_tables import movie_genres, movie_actors, movie_directors

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    # One-to-Many Relationship Section
    reviews = db.relationship('Review', backref='movie')

    # Many-to-Many Relationship Section
    genres = db.relationship('Genre', secondary=movie_genres, backref='movies')
    actors = db.relationship('Actor', secondary=movie_actors, backref='movies')
    directors = db.relationship('Director', secondary=movie_directors, backref='movies')