from django.test import TestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_data = {
            "id": 3,
            "username": "johndoe",
            "email": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "api_key": "abc123xyz789",
            "password": "securepassword123" , 
        }
        self.login_url = reverse('login') 
        self.register_url = reverse('register') 

    def test_register_user_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("username", response.json())
        self.assertIn("email", response.json())

    def test_register_user_missing_field(self):
        """Test registration with missing fields"""
        incomplete_data = {
            "username": "testuser"
        }
        response = self.client.post(self.register_url, incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_invalid_email(self):
        """Test registration with invalid email"""
        invalid_email_data = {
            "username": "testuser",
            "password": "testpassword123",
            "email": "not-an-email"
        }
        response = self.client.post(self.register_url, invalid_email_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_login_success(self):
        """Test successful login"""
        Obj = get_user_model()
        self.user = Obj.objects.create_user(username="test", password="pass")
        login_data = {
            "username": "test",
            "password": "pass"
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertIn("session_id", response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        Obj = get_user_model()
        Obj.objects.create_user(**self.user_data)
        invalid_login_data = {
            "username": self.user_data["username"],
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, invalid_login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

