from rest_framework import serializers
from users.models import User
class UserSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = User 
        fields = ('id', 'username', 'email', 'first_name', 'last_name' , 'api_key' , 'password')
    def create(self, validated_data):
        password = validated_data.pop('password') 
        user = User(**validated_data) 
        user.set_password(password) 
        user.save()  
        return user
class LoginUserSerializer(serializers.Serializer) :
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)