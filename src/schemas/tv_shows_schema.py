from main import ma

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
    actors = ma.Nested('ActorSchema', many=True, exclude=('tv_shows',))
    directors = ma.Nested('DirectorSchema', many=True, exclude=('tv_shows',))
    genres = ma.Nested('GenreSchema', many=True, exclude=('tv_shows',))
    reviews = ma.Nested('ReviewSchema', many=True, exclue=('tv_shows',))


tvshow_schema = TVShowSchema
tvshows_schema = TVShowSchema(many=True)