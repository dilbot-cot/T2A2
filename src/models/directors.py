from main import db

class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)

    # Many-to-Many Relationship Section
    movies = db.relationship('Movie', secondary='movie_directors', back_populates='directors')
    tv_shows = db.relationship('TVShow', secondary='tv_directors', back_populates='directors')