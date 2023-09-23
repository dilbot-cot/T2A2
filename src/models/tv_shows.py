from main import db
from .join_tables import tv_show_directors, tv_show_actors, tv_show_genres

class TV_Show(db.Model):
    __tablename__= "tv_shows"
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)

    # One to Many Relationships
    reviews = db.relationship('Review', backref='tv_show', lazy=True)

    # Many to Many Relationships
    genres = db.relationship('Genre', secondary=tv_show_genres, backref=db.backref('tv_shows', lazy='dynamic'))
    actors = db.relationship('Genre', secondary=tv_show_actors, backref=db.backref('tv_shows', lazy='dynamic'))
    directors = db.relationship('Genre', secondary=tv_show_directors, backref=db.backref('tv_shows', lazy='dynamic'))