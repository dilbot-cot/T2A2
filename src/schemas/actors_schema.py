from main import ma

class ActorSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'name',
            'dob'
        )

actor_schema = ActorSchema
actors_schema = ActorSchema(many=True)