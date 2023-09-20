from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from main import db

# TVDirector Model
class TVDirector(db.Model):
    __tablename__ = 'tv_directors'
    id = db.Column(db.Integer, primary_key=True)

    tv_show_id = db.Column(db.Integer, ForeignKey('tv_shows.id'), nullable=False)
    director_id = db.Column(db.Integer, ForeignKey('directors.id'), nullable=False)

    # Relationships
    tv_show = relationship('TVShow', back_populates='tv_directors')
    director = relationship('Director', back_populates='tv_directors')
