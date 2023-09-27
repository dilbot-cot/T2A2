from main import ma

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
    movies = ma.Nested('MovieSchema', many=True, exclude=('genres',))
    tv_shows = ma.Nested('TVShowSchema', many=True, exclude=('genres',))

genre_schema = GenreSchema
genres_schema = GenreSchema(many=True)