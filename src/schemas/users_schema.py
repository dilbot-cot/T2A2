from main import ma

class UserListSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'username',
            'email',
            'is_admin',
        )

users_list_schema = UserListSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        # Fields to show
        fields = (
            'id',
            'username',
            'email',
            'reviews'
        )

    # Nested fields
    reviews = ma.Nested('ReviewSchema', many=True, only=('id','content','rating','movies','tv_shows'))

user_schema = UserSchema()
users_schema = UserSchema(many=True)