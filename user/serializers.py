from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ShowLogin(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']


class addUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=make_password(validated_data['password']),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.save()
        return user

class updateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'first_name', 'last_name']
