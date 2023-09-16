from main import db
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime

class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, unique=True, nullable=False)
    dob = db.Column(DateTime, nullable=False)

    tv = relationship("TVDirector", back_populates="directors")
    movie = relationship("MovieDirector", back_populates="directors")