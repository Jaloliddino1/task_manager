from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name'
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            're_password',
        )
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('re_password'):
            raise ValidationError('re passport and password doesn\'t match')
        del attrs['re_password']
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise ValidationError('User doesn\'t exist')

        return {"user": user}


class TaskSerializer(serializers.Serializer):
    task_id = serializers.UUIDField()
