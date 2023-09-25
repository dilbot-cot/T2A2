from main import ma
# from schemas import MovieSchema, TVShowSchema

class ActorSchema(ma.Schema):
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
    movies = ma.Nested('MovieSchema', many=True, exclude=('actors',))
    tv_shows = ma.Nested('TVShowSchema', many=True, exclude=('actors',))


actor_schema = ActorSchema
actors_schema = ActorSchema(many=True)