from main import db
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

class Actor(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, unique=True, nullable=False)
    dob = db.Column(DateTime, nullable=False)

    tv = relationship("TVActor", back_populates="actors")
    movie = relationship("MovieActor", back_populates="actors")