from time import timezone

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from pyexpat.errors import messages
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User, Code
from accounts.service import send_email
from django.utils import timezone

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

class Check_user_serializer(serializers.Serializer):
    email = serializers.EmailField()


    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            raise ValidationError('Did not find this type of email')
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        code=Code.objects.create(user=user)
        send_email(
            subject='Password recovery code',
            message= f"{user.username} secret code for user {code.code}",
            to_email = user.email
        )
        return code
class Restore_serilizer(serializers.Serializer):
    code=serializers.CharField(max_length=200,write_only=True)
    password=serializers.CharField(max_length=100,write_only=True)
    re_password=serializers.CharField(max_length=100,write_only=True)

    def validate(self,attrs):
        if not attrs.get('password') == attrs.get('re_password'):
            raise ValidationError('Password not equal re_password')
        return attrs

    def validate_code(self, value):
        try:
            code = Code.objects.get(code=value)
        except Code.DoesNotExist:
            raise ValidationError('Kod topilmadi')

        if code.exp_date < timezone.now():
            raise ValidationError("Codingiz vaqti o‘tib ketgan, qayta yuboring")

        self.instance = code
        return value

    def save(self, attrs):
        user=Code.user.get('user')
        user.set_password(attrs.get('password'))
        user.save()
        return user