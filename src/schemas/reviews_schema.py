from main import ma

class TVShowSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'title',
            'start_date',
            'end_date'
        )

tv_show_schema = TVShowSchema
tv_shows_schema = TVShowSchema(many=True)