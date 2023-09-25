from main import ma

class DirectorSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'name',
            'dob'
        )

director_schema = DirectorSchema
directors_schema = DirectorSchema(many=True)