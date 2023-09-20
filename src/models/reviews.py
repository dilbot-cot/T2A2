from main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    
    content = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, ForeignKey('movies.id'), nullable=True)
    tv_id = db.Column(db.Integer, ForeignKey('tv_shows.id'), nullable=True)

    # Relationships
    user = relationship('User', back_populates='reviews')
    movie = relationship('Movie', back_populates='reviews')
    tv_show = relationship('TVShow', back_populates='reviews')