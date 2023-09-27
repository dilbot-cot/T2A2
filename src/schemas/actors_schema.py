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
    movies = ma.Nested('MovieSchema', many=True, only=('id','title','release_date'))
    tv_shows = ma.Nested('TVShowSchema', many=True, only=('id','title','start_date','end_date'))


actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)