from rest_framework import generics , status
from posts.serializers import PostSerializer
from posts.models import Post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework_api_key.permissions import  HasAPIKey
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# Create your views here.
class PostListView(generics.ListAPIView)  :
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all() 


class PostDetailView(generics.RetrieveAPIView):
    permission_classes = [HasAPIKey]  
    serializer_class = PostSerializer
    queryset = Post.objects.all()   


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
