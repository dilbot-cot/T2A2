from main import ma

class MovieListSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'title',
            'release_date'
        )

movies_list_schema = MovieListSchema(many=True)

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
    actors = ma.Nested('ActorListSchema', many=True)
    directors = ma.Nested('DirectorListSchema', many=True)
    genres = ma.Nested('GenreListSchema', many=True)
    reviews = ma.Nested('ReviewSchema', many=True, only=('id', 'content', 'rating'))

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)