from main import ma

class UserSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'username',
            'email',
            'password',
            'is_admin'
        )
user_schema = UserSchema
users_schema = UserSchema(many=True)