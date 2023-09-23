from main import db

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tv_id = db.Column(db.Integer, db.ForeignKey('tv_shows.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
