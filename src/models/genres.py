from main import db

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    movies = db.relationship('Movie', secondary='movie_genres', back_populates='genres')
    tv_shows = db.relationship('TVShow', secondary='tv_genres', back_populates='genres')