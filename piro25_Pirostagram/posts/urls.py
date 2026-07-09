from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.post_create, name='post_create'),
    path('edit/<int:post_id>/', views.post_update, name='post_update'),
    path('delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('like/<int:post_id>/', views.post_like, name='post_like'),
    path('comment/<int:post_id>/', views.comment_create, name='comment_create'),
    path('search/', views.user_search, name='user_search'),
]