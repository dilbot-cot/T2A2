from main import db, bcrypt
from flask import Blueprint
from models.__innit__ import Actor, Director, Genre, Movie, Review, TVShow, User
from datetime import date

db_commands = Blueprint("db", __name__)

@db_commands .cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables Dropped")

@db_commands .cli.command("seed")
def seed_db():
    actor1 = Actor(
        name = "Mark Hamill",
        dob = date(1951, 9, 25)
    )
    actor2 = Actor(
        name = "Harrison Ford",
        dob = date(1942, 7, 13)
    )

    director1 = Director(
        name = "George Lucas",
        dob = date(1944, 5, 14)
    )
    director2 = Director(
        name = "Steven Spielberg",
        dob = date(1946, 12, 18)
    )
    director3 = Director(
        name = "Bill Lawrence",
        dob = date(1968, 12, 26)
    )

    genre1 = Genre(
        name = "Action"
    )
    genre2 = Genre(
        name = "Adventure"
    )
    genre3 = Genre(
        name = "Fantasy"
    )
    genre4 = Genre(
        name = "Sci-Fi"
    )
    genre5 = Genre(
        name = "Animation"
    )
    genre6 = Genre(
        name = "Crime"
    )
    genre7 = Genre(
        name = "Family"
    )
    genre8 = Genre(
        name = "Mystery"
    )
    genre9 = Genre(
        name = "Comedy"
    )
    genre10 = Genre(
        name = "Drama"
    )
    
    movie1 = Movie(
        title = "Star Wars: Episode IV - A New Hope",
        release_date = date(1978, 1, 28)
    )
    movie2 = Movie(
        title = "Indiana Jones and the Temple of Doom",
        release_date = date(1984, 6, 15)
    )

    tvshow1 = TVShow(
        title = "Batman: The Animated Series",
        start_date = date(1992, 9, 5),
        end_date = date(1995, 9, 15)
    )
    tvshow2 = TVShow(
        title = "Shrinking",
        start_date = date(2023, 1, 27)
    )

    user1 = User(
        username = "Awesome McAwesome",
        email = "admin@email.com",
        password = bcrypt.generate_password_hash("P@ssw0rd").decode("utf-8"),
        is_admin = True
    )
    user2 = User(
        username = "Random User123",
        email = "user@email.com",
        password = bcrypt.generate_password_hash("123456").decode("utf-8"),
    )

    review1 = Review(
        content = "I really liked this movie, it is one of my favourite Star Wars films",
        rating = 4
    )
    review2 = Review(
        content = "I liked this movie, it is one of my favourite Indiana Jones films",
        rating = 3
    )
    review3 = Review(
        content = "I have only watched bits of this TV Show, but I really liked what I've seen!",
        rating = 3
    )
    review4 = Review(
        content = "Too early for me to tell on this show"
    )

    db.session.add_all([
        actor1, actor2,
        director1, director2, director3,
        movie1, movie2,
        tvshow1, tvshow2,
        user1, user2,
        review1, review2, review3, review4,
        genre1, genre2, genre3, genre4, genre5, genre6, genre7, genre8, genre9, genre10
        ])
    db.session.commit()
    print("Tables seeded")