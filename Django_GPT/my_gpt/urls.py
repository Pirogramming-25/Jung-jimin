from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("sentiment/", views.sentiment, name="sentiment"),
    path("sentiment/run/", views.sentiment_run, name="sentiment_run"),

    path("summarize/", views.summarize, name="summarize"),
    path("summarize/run/", views.summarize_run, name="summarize_run"),

    path("moderate/", views.moderate, name="moderate"),
    path("moderate/run/", views.moderate_run, name="moderate_run"),

    path("combo/", views.combo, name="combo"),
    path("combo/run/", views.combo_run, name="combo_run"),
]