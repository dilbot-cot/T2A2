from main import ma
# from schemas import MovieSchema, TVShowSchema

class DirectorSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'name',
            'dob',          
            'movies',
            'tv_shows'
        )
    
    # Nested fields
    movies = ma.Nested('MovieSchema', many=True, exclude=('directors',))
    tv_shows = ma.Nested('TVShowSchema', many=True, exclude=('directors',))

director_schema = DirectorSchema
directors_schema = DirectorSchema(many=True)