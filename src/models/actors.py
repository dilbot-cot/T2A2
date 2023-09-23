from main import db

class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
