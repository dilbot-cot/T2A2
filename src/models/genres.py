from main import db
from sqlalchemy.orm import relationship

class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, unique=True, nullable=False)

    tv = relationship("TV", back_populates="genres")
    movie = relationship("Movie", back_populates="genres")