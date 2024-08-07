from rest_framework import serializers
# from django.contrib.auth import get_user_model
from .models import User,FriendRequest

# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'groups', 'user_permissions', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'timestamp']
