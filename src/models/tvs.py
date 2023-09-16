from main import db
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship

class TV(db.Model):
    __tablename__ = "tvs"
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    start_date = db.Column(DateTime, nullable=False)
    end_date = db.Column(DateTime, nullable=True)
    genre = db.Column(db.Integer, ForeignKey('genres.id'), nullable=False)

    genre = relationship("Genre", back_populates="tvs")