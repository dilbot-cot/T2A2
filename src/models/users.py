from main import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False) #password length will be handled by routes
    is_admin = db.Column(db.Boolean, default=False)

    reviews = relationship("Review", back_populates="user")