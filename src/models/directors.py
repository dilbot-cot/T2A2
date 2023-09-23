from main import db

class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)