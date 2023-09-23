from main import db, bcrypt
from flask import Blueprint
from models import Actor, Director, Genre, Movie, Review, TV_Show, User
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
    db.session.add_all([])
    db.session.commit()
    print("Tables seeded")