from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from .models import Post
from .serializers import PostSerializer
from django.contrib.auth.models import User
# get user model from ? 
from django.contrib.auth import get_user_model
class PostViewTests(TestCase):
    def setUp(self):
        Obj = get_user_model()
        self.user = Obj.objects.create_user(username="test", password="test")
        self.post = Post.objects.create(title="Test Post", content="Content", author=self.user)
        _, self.key = APIKey.objects.create_key(name="test")
        self.client = APIClient()
        
    def test_list_posts_unauthenticated(self):
        """Ensure unauthenticated users cannot access the list view"""
        response = self.client.get(reverse("post-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_posts_authenticated(self):
        """Ensure authenticated users can access the list view"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("post-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Post.objects.count())

    def test_detail_post_unauthenticated(self):
        """Ensure unauthenticated users cannot access the detail view"""
        response = self.client.get(reverse("post-detail", kwargs={"pk": self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_post_with_api_key(self):
        print( """Ensure users with valid API keys can access the detail view""" )
        authorization = f"Api-Key {self.key}"
        response = self.client.get(reverse("post-detail", kwargs={"pk": self.post.pk}),HTTP_AUTHORIZATION=authorization,format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.post.title)

    def test_create_post_unauthenticated(self):
        """Ensure unauthenticated users cannot create a post"""
        response = self.client.post("/posts/create/", {"title": "My New Post", "content": "This is the content of the post" , "author" : self.user.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_authenticated(self):
        """Ensure authenticated users can create a post"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/posts/create/", {"title": "My New Post", "content": "This is the content of the post" , "author" : self.user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_serializer_valid(self):
        """Ensure the serializer is valid with valid data"""
        data = {"title": "Test", "content": "Content", "author": self.user.id}
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
    def test_serializer_invalid(self):
        """Ensure the serializer is invalid with invalid data"""
        data = {"title": "", "content": "Content", "author": self.user.id}
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    def test_model(self):
        post = Post.objects.get(title="Test Post")
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "Content")
        self.assertEqual(post.author, self.user)
    