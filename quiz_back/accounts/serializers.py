from rest_framework import serializers
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(max_length=50, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password','username')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.pop('username')
        user = User.objects.create_user(**validated_data)
        # 회원가입과 동시에 Profile 생성
        Profile.objects.create(user=user, username=username)
        return user