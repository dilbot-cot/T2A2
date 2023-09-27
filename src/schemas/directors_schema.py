from main import ma

class DirectorListSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'name',
            'dob'
        )

directors_list_schema = DirectorListSchema(many=True)

class DirectorListSchema(ma.Schema):
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
    movies = ma.Nested('MovieListSchema', many=True)
    tv_shows = ma.Nested('TVShowListSchema', many=True)

director_schema = DirectorListSchema()
directors_schema = DirectorListSchema(many=True)