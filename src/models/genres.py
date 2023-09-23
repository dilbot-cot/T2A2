from main import db

class Genre(db.Model):
    __tablename__= "genres"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)