from main import ma

class GenreListSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'name'
        )

genres_list_schema = GenreListSchema(many=True)

class GenreSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'name',
            'movies',
            'tv_shows'
        )
    
    # Nested fields
    movies = ma.Nested('MovieListSchema', many=True)
    tv_shows = ma.Nested('TVShowListSchema', many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)