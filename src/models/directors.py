from main import db

class Director(db.Model):
    __tablename__= "directors"
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)