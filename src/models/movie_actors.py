from main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class MovieActor(db.Model):
    __tablename__ = 'movie_actors'
    id = db.Column(db.Integer, primary_key=True)
    
    movie_id = db.Column(db.Integer, ForeignKey('movies.id'), nullable=False)
    actor_id = db.Column(db.Integer, ForeignKey('actors.id'), nullable=False)

    # Relationships
    movie = relationship('Movie', back_populates='movie_actors')
    actor = relationship('Actor', back_populates='movie_actors')
