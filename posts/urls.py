from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),  
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
]