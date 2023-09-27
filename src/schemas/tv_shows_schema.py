from main import ma

class TVShowListSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'title',
            'start_date',
            'end_date'
        )

tvshows_list_schema = TVShowListSchema(many=True)

class TVShowSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'title',
            'start_date',
            'end_date',
            'actors',
            'directors',
            'genres',
            'reviews'
        )

    # Nested fields
    # Nested fields
    actors = ma.Nested('ActorListSchema', many=True)
    directors = ma.Nested('DirectorListSchema', many=True)
    genres = ma.Nested('GenreListSchema', many=True)
    reviews = ma.Nested('ReviewSchema', many=True, only=('id', 'content', 'rating', 'user'))

tvshow_schema = TVShowSchema()
tvshows_schema = TVShowSchema(many=True)