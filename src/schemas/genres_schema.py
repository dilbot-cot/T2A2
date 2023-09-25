from main import ma

class MovieSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'title',
            'release_date'
        )

movie_schema = MovieSchema
movies_schema = MovieSchema(many=True)