from main import db

class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)

    # Many-to-Many Relationship Section
    movies = db.relationship('Movie', secondary='movie_actors', back_populates='actors')
    tv_shows = db.relationship('TVShow', secondary='tv_actors', back_populates='actors')