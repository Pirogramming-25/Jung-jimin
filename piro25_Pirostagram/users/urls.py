from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('search/', views.user_search, name='user_search'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
]