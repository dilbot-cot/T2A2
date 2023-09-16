from main import db
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    release = db.Column(DateTime, nullable=False)
    genre_id = db.Column(db.Integer, ForeignKey('genres.id'), nullable=False)

    genre = relationship("Genre", back_populates="movies")