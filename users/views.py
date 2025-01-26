from rest_framework import generics , status
from users.serializers import UserSerializer , LoginUserSerializer
from users.models import User
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login , logout
   
class UserCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({
                    'message': 'Login successful',
                    'session_id': request.session.session_key,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                    },
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LogoutAPIView(APIView):
    def get(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
# /api/token/ jwt_token
#  /login/ user_session
# /admin/  --> API KEY
