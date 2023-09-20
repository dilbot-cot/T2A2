from sqlalchemy.orm import relationship
from main import db

# Genre Model
class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    # Relationships
    movies = relationship('Movie', back_populates='genre')
    tv_shows = relationship('TVShow', back_populates='genre')