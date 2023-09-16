from main import db
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship

class TVDirector(db.Model):
    __tablename__ = "tv_directors"
    id = db.Column(db.Integer, primary_key=True)

    tv_id = db.Column(db.Integer, ForeignKey('tvs.id'), nullable=False)
    director_id = db.Column(db.Integer, ForeignKey('directors.id'), nullable=False)

    tv = relationship("TV", back_populates="tv_directors")
    director = relationship("Director", back_populates="tv_directors")