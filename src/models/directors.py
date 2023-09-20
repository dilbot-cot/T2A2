from main import db
from sqlalchemy import Date
from sqlalchemy.orm import relationship


# Director Model
class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    dob = db.Column(Date, nullable=False)

    # Relationships
    movie_directors = relationship('MovieDirector', back_populates='director')
    tv_directors = relationship('TVDirector', back_populates='director')
