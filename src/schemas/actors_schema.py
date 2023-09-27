from main import ma

class ActorListSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'name',
            'dob'
        )

actors_list_schema = ActorListSchema(many=True)

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
    movies = ma.Nested('MovieListSchema', many=True)
    tv_shows = ma.Nested('TVShowListSchema', many=True)


actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)