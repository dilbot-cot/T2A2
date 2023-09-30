from main import db
from sqlalchemy import Table, Column, Integer, ForeignKey

tv_genres = Table('tv_genres', db.Model.metadata,
    Column('tv_id', Integer, ForeignKey('tv_shows.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

movie_genres = Table('movie_genres', db.Model.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

tv_actors = Table('tv_actors', db.Model.metadata,
    Column('tv_id', Integer, ForeignKey('tv_shows.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

movie_actors = Table('movie_actors', db.Model.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

tv_directors = Table('tv_directors', db.Model.metadata,
    Column('tv_id', Integer, ForeignKey('tv_shows.id')),
    Column('director_id', Integer, ForeignKey('directors.id'))
)

movie_directors = Table('movie_directors', db.Model.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('director_id', Integer, ForeignKey('directors.id'))
)