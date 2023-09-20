from main import db
from sqlalchemy import Date
from sqlalchemy.orm import relationship


# Director Model
class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    dob = db.Column(Date, nullable=False)

    # Relationships
    movie_actors = relationship('MovieActor', back_populates='actor')
    tv_actors = relationship('TVActor', back_populates='actor')
