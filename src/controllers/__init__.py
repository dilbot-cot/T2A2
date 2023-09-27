from .actors_controller import actors
from .admin_controller import admin
from .user_controller import user
from .directors_controller import directors
from .home_controller import home
from .genres_controller import genres
from .movies_controller import movies
from .tv_shows_controller import tv_shows
from .reviews_controller import review

registerable_controllers = [
    actors,
    admin, 
    user,
    directors, 
    home, 
    genres,
    movies, 
    tv_shows, 
    review
]