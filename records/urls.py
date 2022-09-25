from django.urls import path
from . import views

app_name = "records"

# Register URL patterns
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("result/", views.ResultView.as_view(), name="result"),
    path("medal/", views.MedalView.as_view(), name="medal"),
    path("score/", views.ScoreView.as_view(), name="score"),
    path("athlete/", views.AthleteView.as_view(), name="athlete"),
    path("team/", views.TeamView.as_view(), name="team"),
]
