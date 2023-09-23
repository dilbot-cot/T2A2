from main import db

class Review(db.Model):
    __tablename__= "reviews"
    id = db.Column(db.Integer, primary_key=True)
    
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)

    # Forign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tv_show_id = db.Column(db.Integer, db.ForeignKey('tv_show.id'), nullable=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=True)