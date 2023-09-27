from main import db

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    # One-to-Many Relationship Section
    reviews = db.relationship('Review', backref='movie')

    # Many-to-Many Relationship Section
    genres = db.relationship('Genre', secondary='movie_genres', back_populates='movies')
    actors = db.relationship('Actor', secondary='movie_actors', back_populates='movies')
    directors = db.relationship('Director', secondary='movie_directors', back_populates='movies')