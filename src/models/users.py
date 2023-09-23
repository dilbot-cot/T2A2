from main import db

class User(db.Model):
    __tablenames__= "users"
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    reviews = db.relationship('Review', backref='author', lazy=True)
