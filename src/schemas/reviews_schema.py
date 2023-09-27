from main import ma

class ReviewSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'content',
            'rating',
            'movie',
            'tv_show',
            'user'
        )
    
    # Nested fields
    movie = ma.Nested('MovieSchema', only=('id', 'title', 'release_date'))
    tv_show = ma.Nested('TVShowSchema', only=('id', 'title', 'start_date', 'end_date'))
    user = ma.Nested('UserSchema', only=('id', 'username'))

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)