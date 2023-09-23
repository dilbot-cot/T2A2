from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import relationship
from main import db

# TVShow Model
class TVShow(db.Model):
    __tablename__ = 'tv_shows'
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    start_date = db.Column(Date, nullable=False)
    end_date = db.Column(Date, nullable=True)

    # Relationships
    genre = relationship('Genre', back_populates='tv_shows')
    reviews = relationship('Review', back_populates='tv_show')
    tv_actors = relationship('TVActor', back_populates='tv_show')
    tv_directors = relationship('TVDirector', back_populates='tv_show')
