from main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class TVActor(db.Model):
    __tablename__ = "tv_actors"
    id = db.Column(db.Integer, primary_key=True)

    tv_id = db.Column(db.Integer, ForeignKey('tvs.id'), nullable=False)
    actor_id = db.Column(db.Integer, ForeignKey('actors.id'), nullable=False)

    tv = relationship("TV", back_populates="tv_actors")
    actor = relationship("Actor", back_populates="tv_actors")