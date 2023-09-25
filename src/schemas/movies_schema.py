from main import ma
# from schemas import ActorSchema, DirectorSchema, GenreSchema, ReviewSchema

class MovieSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'title',
            'release_date',
            'actors',
            'directors',
            'genres',
            'reviews'
        )

    # Nested fields
    actors = ma.Nested('ActorSchema', many=True, exclude=('movies',))
    directors = ma.Nested('DirectorSchema', many=True, exclude=('movies',))
    genres = ma.Nested('GenreSchema', many=True, exclude=('movies',))
    reviews = ma.Nested('ReviewSchema', many=True, exclue=('movies',))

movie_schema = MovieSchema
movies_schema = MovieSchema(many=True)