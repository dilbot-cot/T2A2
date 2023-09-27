from main import ma

class UserSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'username',
            'email',
            'password',
            'is_admin',
            'reviews'
        )

    # Nested fields
    reviews = ma.Nested('ReviewSchema', many=True, exclude=('user',))

user_schema = UserSchema
users_schema = UserSchema(many=True)