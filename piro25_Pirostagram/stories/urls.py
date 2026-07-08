from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('create/', views.story_create, name='story_create'),
    path('delete/<int:story_id>/', views.story_delete, name='story_delete'),
]