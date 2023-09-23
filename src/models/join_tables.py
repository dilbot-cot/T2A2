from main import db
# I had played with each of these joins being separate python scripts, however as this is a small/medium project it made more sense from a DRY principle to have this as a single file.

# Join table for TV_Shows and Genres
tv_show_genres = db.Table('tv_show_genres',
    db.Column('tv_show_id', db.Integer, db.ForeignKey('tv_show.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

# Join table for Movies and Genres
movie_genres = db.Table('movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

# Join table for TV_Shows and Actors
tv_show_actors = db.Table('tv_show_actors',
    db.Column('tv_show_id', db.Integer, db.ForeignKey('tv_show.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True)
)

# Join table for Movies and Actors
movie_actors = db.Table('movie_actors',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True)
)

# Join table for TV_Shows and Directors
tv_show_directors = db.Table('tv_show_directors',
    db.Column('tv_show_id', db.Integer, db.ForeignKey('tv_show.id'), primary_key=True),
    db.Column('director_id', db.Integer, db.ForeignKey('director.id'), primary_key=True)
)

# Join table for Movies and Directors
movie_directors = db.Table('movie_directors',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('director_id', db.Integer, db.ForeignKey('director.id'), primary_key=True)
)