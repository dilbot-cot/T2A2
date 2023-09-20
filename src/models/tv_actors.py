from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from main import db

# TVActor Model
class TVActor(db.Model):
    __tablename__ = 'tv_actors'
    id = db.Column(db.Integer, primary_key=True)

    tv_show_id = db.Column(db.Integer, ForeignKey('tv_shows.id'), nullable=False)
    actor_id = db.Column(db.Integer, ForeignKey('actors.id'), nullable=False)

    # Relationships
    tv_show = relationship('TVShow', back_populates='tv_actors')
    actor = relationship('Actor', back_populates='tv_actors')