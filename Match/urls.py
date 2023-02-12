from django.urls import path
from Match import views

urlpatterns = [
    path('', views.home, name='matchhome'),
    path('start/', views.startmatch),
    path('start/send_lineup/<str:team1>/<str:team2>/', views.set_lineup),
    path('start/<str:team1>/<str:team2>/', views.handle_match),
    path('start/<str:team1>/<str:team2>/scorecard_json/', views.get_json_response, name='scorecard_json'),
    path('start/<str:team1>/<str:team2>/get_player_json/<str:name>/', views.get_player_json, name='player_json'),
]