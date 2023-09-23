from main import db
from .join_tables import movie_actors, movie_directors, movie_genres

class Movie(db.Model):
    __tablename__= "movies"
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    # One to Many Relationships
    reviews = db.relationship('Review', backref='movie', lazy=True)

    # Many to Many Relationships
    genres = db.relationship('Genre', secondary=movie_genres, backref=db.backref('movies', lazy='dynamic'))
    actors = db.relationship('Genre', secondary=movie_actors, backref=db.backref('movies', lazy='dynamic'))
    directors = db.relationship('Genre', secondary=movie_directors, backref=db.backref('movies', lazy='dynamic'))