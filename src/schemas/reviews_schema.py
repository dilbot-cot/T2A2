from main import ma

class ReviewSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'content',
            'rating',
            'movies',
            'tv_shows',
            'user'
        )
    
    # Nested fields
    movies = ma.Nested('MovieSchema', only=('id', 'title', 'release_date'))
    tv_shows = ma.Nested('TVShowSchema', only=('id', 'title', 'start_date', 'end_date'))
    user = ma.Nested('UserSchema', only=('id', 'username'))

review_schema = ReviewSchema
reviews_schema = ReviewSchema(many=True)