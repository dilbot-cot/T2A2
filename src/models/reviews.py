from main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, ForeignKey('movies.id'), nullable=False)
    tv_id = db.Column(db.Integer, ForeignKey('tvs.id'), nullable=False)

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")
    tv = relationship("TV", back_populates="reviews")