from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User

class StatelessJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # Return a stateless user object just containing the ID from the token
        # This prevents the DB lookup that fails in independent microservices
        user = User()
        user.id = validated_token.get('user_id')
        return user
