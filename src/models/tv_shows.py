from main import db
from .join_tables import tv_genres, tv_actors, tv_directors

class TVShow(db.Model):
    __tablename__ = 'tv_shows'
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)

    # One-to-Many Relationship Section
    reviews = db.relationship('Review', backref='tv_show')

    # Many-to-Many Relationship Section
    genres = db.relationship('Genre', secondary=tv_genres, backref='tv_shows')
    actors = db.relationship('Actor', secondary=tv_actors, backref='tv_shows')
    directors = db.relationship('Director', secondary=tv_directors, backref='tv_shows')